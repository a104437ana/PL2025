# variáveis globais da ast
global_vars = {}        # dicionário ID -> posição no global pointer
global_vars_type = {}   # dicionário ID -> tipo da variável
known_functions = {}    # dicionário ID -> posição do retorno no global pointer
func_types = {}         # dicionário ID -> tipo de retorno da função
array_init = {}         # dicionário ID -> posição inicial do array
array_type = {}         # dicionário ID -> tipo do array
last_global_pointer = 0 # última posição do global pointer
local_scope = ""        # função ou procedimento onde está
func_params = {}        # dicionário ID -> posição no stack pointer
func_vars = {}          # dicionário ID -> posição no stack pointer
func_vars_type = {}     # dicionário ID -> tipo da variável
func_vars_number = {}   # dicionário ID -> número de variáveis da função

# metodos globais da ast


class Program:
    def __init__(self, id, declarations, code):
        self.id = id                        # ID do programa
        self.declarations = declarations    # lista de classes Declaration
        self.code = code                    # classe CodeBlock
    
    def generateVmCode(self):
        code = ""
        heap = ""
        for decl in self.declarations:
            if isinstance(decl, Variables):
                code += f"\n{decl.generateVmCodePush()}"
                heap += f"\n{decl.generateVmCodeHeap()}"
        code += f"\nSTART\n"
        code += f"{heap}\n"
        code += f"{self.code.generateVmCode()}"
        code += f"STOP\n\n"
        for decl in self.declarations:
            if isinstance(decl, Function):
                code += f"{decl.generateVmCode()}\n"
            elif isinstance(decl, Procedure):
                code += f"\n" # ver como fazer

        return code
    
    def anasem(self):
        errors = ""
        for decl in self.declarations:
            if isinstance(decl, Variables):
                decl.anasem()
            elif isinstance(decl, Function):
                pass # ver como fazer
            elif isinstance(decl, Procedure):
                pass # ver como fazer
        errors = self.code.anasem()
        if errors:
            print(f"\033[1;31mSemantic error - {errors}\033[0m")
        return errors

    def __str__(self):
        prog = f"program {self.id};\n"
        for decl in self.declarations:
            prog += f"\n{str(decl)}"
        prog += f"\n{str(self.code)}."
        return prog

    __repr__ = __str__

class Declaration:
    pass

class Variable():
    def __init__(self, id, type, is_array=False, array_size=0, array_init=0, array_type=None, value=None):
        self.id = id                    # ID da variável
        self.type = type                # tipo da variável
        self.is_array = is_array        # se é um array
        self.array_size = array_size    # tamanho do array
        self.array_init = array_init    # primeiro índice do array
        self.array_type = array_type    # tipo de dados do array
        self.value = value              # valor

    def generateVmCode(self):
        return ""

    def generateVmCodePush(self):
        code = ""
        if self.type == "string":
            code += f'PUSHI 0'
        elif self.type == "character":
            code += f'PUSHS ""'
        elif self.type == "integer":
            code += f"PUSHI 0"
        elif self.type == "real":
            code += f"PUSHF 0.0"
        elif self.type == "boolean":
            code += f"PUSHI 0"
        elif self.type == "array":
            code += f"PUSHI 0"
        return code

    def generateVmCodeHeap(self):
        code = ""
        global global_vars, array_init, array_type, func_vars, local_scope
        if local_scope == "":
            var_pointer = global_vars[str(self.id)]
            array_init[self.id] = self.array_init
            array_type[self.id] = self.array_type
            code += f"PUSHI {self.array_size}\n"
            code += "ALLOCN\n"
            code += f"STOREG {var_pointer}\n"
        else:
            var_pointer = func_vars[str(self.id)]
            array_init[self.id] = self.array_init
            array_type[self.id] = self.array_type
            code += f"PUSHI {self.array_size}\n"
            code += "ALLOCN\n"
            code += f"STOREL {var_pointer}\n"
        return code

    def __str__(self):
        var = f"{self.id}: {self.type}"
        if self.is_array:
            var += f"[{self.array_init}..{self.array_init+self.array_size-1}] of {self.array_type};"
        return var

    __repr__ = __str__

class Variables(Declaration):
    def __init__(self, variables=None):
        self.variables = variables if variables is not None else {} # dicionário ID -> classe Variable
    
    def add(self, variable: Variable):
        if isinstance(variable, Variable):
            self.variables[variable.id] = variable
        elif isinstance(variable, Variables):
            for id, var in variable.variables.items():
                if var.id not in self.variables:
                    self.variables[var.id] = var
                else:
                    raise Exception(f"Variable {var.id} already defined")

    def items(self):
        return self.variables.items()

    def generateVmCode(self):
        return ""
    
    def anasem(self):
        global global_vars_type
        for id, var in self.variables.items():
            global_vars_type[var.id] = var.type
        return ""

    def generateVmCodePush(self):
        global last_global_pointer, global_vars, global_vars_type, local_scope
        code = ""
        for id, var in self.variables.items():
            if local_scope == "":
                code += var.generateVmCodePush() + f" // variavel {var.id}\n"
                global_vars[var.id] = last_global_pointer
                global_vars_type[var.id] = var.type
                last_global_pointer += 1
        if local_scope != "":
            code += f"PUSHN {len(self.variables)}\n"
        return code

    def generateVmCodeHeap(self):
        code = ""
        for id, var in self.variables.items():
            if var.is_array:
                code += f"// heap variavel {var.id}\n"
                code += f"{var.generateVmCodeHeap()}"
        return code

    def funcProcVars(self, idFunc):
        global func_vars, func_vars_type
        last_stack_pointer = 0
        func_vars[idFunc] = {}
        func_vars_type[idFunc] = {}
        for id, var in self.variables.items():
            func_vars[idFunc][var.id] = last_stack_pointer
            func_vars_type[idFunc][var.id] = var.type
            last_stack_pointer += 1

    def funcProcParams(self, idFunc):
        global func_params
        last_stack_pointer = -len(self.variables)
        for id, var in self.variables.items():
            func_vars[idFunc][var.id] = last_stack_pointer
            func_vars_type[idFunc][var.id] = var.type
            last_stack_pointer += 1

    def isVariable(self, id):
        return id in self.variables.keys()

    def __str__(self):
        if len(self.variables.items()) > 0:
            vars = f"var\n"
        else:
            return ""
        for id, var in self.variables.items():
            vars += "\t" + str(var) + "\n"
        return vars

    def strParams(self):
        params = ""
        for i, (id, param) in enumerate(self.variables.items()):
            if i != 0:
                params += " "
            params += str(param)
            if i != len(self.variables)-1:
                params += ";"
        return params

    __repr__ = __str__

class Function(Declaration):
    def __init__(self, id, parameters, return_type, vars, algorithm):
        self.id = id                        # ID da função
        self.parameters = parameters        # classe Variables com as variáveis dos parametros
        self.return_type = return_type      # tipo de retorno
        self.vars = vars                    # classe Variables com as variáveis da função
        self.algorithm = algorithm          # classe CodeBlock
        global last_global_pointer, known_functions, func_vars_number
        known_functions[str(self.id).lower()] = last_global_pointer
        func_types[str(self.id).lower()] = self.return_type
        last_global_pointer += 1
        self.vars.funcProcVars(str(self.id).lower())
        self.parameters.funcProcParams(str(self.id).lower())
        func_vars_number[str(self.id).lower()] = len(self.vars.variables)

    def generateVmCode(self):
        code = ""
        heap = ""
        global local_scope
        local_scope = str(self.id).lower()
        code += f"{local_scope}:\n"
        code += f"\n{self.vars.generateVmCodePush()}"
        heap += f"\n{self.vars.generateVmCodeHeap()}"
        code += f"{heap}\n"
        code += f"{self.algorithm.generateVmCode()}"
        code += f"RETURN\n"
        local_scope = ""

        return code

    def __str__(self):
        func = f"function {self.id}({self.parameters.strParams()}): {self.return_type};\n"
        func += f"{str(self.vars)}\n"
        func += f"{str(self.algorithm)};\n"
        return func

    __repr__ = __str__

class Procedure(Declaration):
    def __init__(self, id, parameters, vars, algorithm):
        self.id = id                    # ID do procedimento
        self.parameters = parameters    # classe Variables com as variáveis dos parametros
        self.vars = vars                # classe Variables com as variáveis da função
        self.algorithm = algorithm      # classe CodeBlock
        global known_functions, func_vars_number
        known_functions[str(self.id).lower()] = -1
        func_types[str(self.id).lower()] = "none"
        func_vars_number[str(self.id).lower()] = len(self.vars.variables)

    def generateVmCode(self):
        code = ""
        heap = ""
        global local_scope
        local_scope = str(self.id).lower()
        code += f"{local_scope}:\n"
        code += f"\n{self.vars.generateVmCodePush()}"
        heap += f"\n{self.vars.generateVmCodeHeap()}"
        code += f"{heap}\n"
        code += f"{self.algorithm.generateVmCode()}"
        code += f"RETURN\n"
        local_scope = ""

        return code

    def __str__(self):
        proc = f"procedure {self.id}({self.parameters.strParams()});\n"
        proc += f"{str(self.vars)}\n"
        proc += f"{str(self.algorithm)};\n"
        return proc

    __repr__ = __str__

class Algorithm:
    def __init__(self, statements=None):
        self.statements = statements if statements is not None else []  # lista de classes Statement

    def add(self, statement):
        if statement is not None:
            self.statements.append(statement)
            
    def anasem(self):
        errors = ""
        for statement in self.statements:
            errors = statement.anasem()
            if errors:
                if errors[0] == "procedure":
                    return ""
                elif errors in ["integer","real","boolean","string"]:
                    return ""
                else:
                    return errors
        return errors
    
    def generateVmCode(self):
        code = ""
        for statement in self.statements:
            code += f"{statement.generateVmCode()}\n"
        return code

    def __str__(self):
        algorithm = ""
        for statement in self.statements:
            algorithm += f"{str(statement)}\n"
        return algorithm

    __repr__ = __str__

class Statement:
    pass

class Assignment(Statement):
    def __init__(self, id, expr, array_pos=None, pos_type=None):
        self.id = id        # ID da variável do assignment
        self.expr = expr    # classe Expression
        self.array_pos = array_pos
        self.pos_type = pos_type
    
    def anasem(self):
        global global_vars_type
        if not (self.id in global_vars_type.keys()):
            return f"This variable was not declared before: '{self.id}'"
        var_type = global_vars_type[str(self.id)]
        var_type2 = self.expr.anasem()
        if not var_type2 in ["integer","boolean","real","string"]:
            return var_type2
        if var_type != var_type2:
            if not (var_type == "real" and var_type2=="integer"):
                return f"Incompatible types: cannot assign value of type '{var_type2}' to variable '{self.id}' of type '{var_type}': {self.id} := {self.expr}"
        return var_type

    def generateVmCode(self):
        code = ""
        global global_vars, global_vars_type, array_init, func_vars, func_vars_type, local_scope
        if local_scope == "":
            var_pointer = global_vars[str(self.id)]
            var_type = global_vars_type[str(self.id)]
            scope = "G"
        else:
            if str(self.id).lower() == local_scope:
                var_pointer = known_functions[str(self.id).lower()]
                var_type = func_types[str(self.id).lower()]
                scope = "G"
            else:
                var_pointer = func_vars[local_scope][str(self.id)]
                var_type = func_vars_type[local_scope][str(self.id)]
                scope = "L"
        if var_type != "array":
            code += self.expr.generateVmCode()
            code += f"STORE{scope} {var_pointer}\n"
        elif var_type == "array":
            init = array_init[self.id]
            code += f"PUSH{scope} {var_pointer}\n"
            pos = f"PUSHI {self.array_pos}\n"
            if self.pos_type == "id":
                if str(self.array_pos) in global_vars.keys():
                    id_pointer = global_vars[str(self.array_pos)]
                elif str(self.array_pos) in func_vars[local_scope].keys():
                    id_pointer = func_vars[local_scope][str(self.array_pos)]
                pos = f"PUSH{scope} {id_pointer}\n"
            code += pos
            code += f"PUSHI {init}\n"
            code += "SUB\n"
            code += self.expr.generateVmCode()
            code += "STOREN\n"
        return code

    def __str__(self):
        assign = f"{self.id} := {str(self.expr)};"
        return assign

    __repr__ = __str__

class Loop(Statement):
    nextID = 0

    def __init__(self, loop_type, cond, statement=None, assignment=None, for_type=None):
        self.loop_type = loop_type                                      # tipo do loop
        self.cond = cond                                                # classe Expression
        self.statement = statement if statement is not None else []     # lista de classes Statement
        self.assignment = assignment                                    # classe Assignment
        self.for_type = for_type                                        # string tipo de ciclo for
        self.loopID = Loop.nextID
        Loop.nextID += 1
        
    def anasem(self):
        if self.assignment != None:
            errors = self.assignment.anasem()
            if errors and not errors in ["integer","real","boolean","string"]:
                return errors
            if errors in ["real","boolean","string"]:
                return f"Incompatible types: got '{errors}' expected 'integer': {self.loop_type} {self.assignment} {self.for_type} {self.cond}"
        c = self.cond.anasem()
        if c not in ["integer","boolean","real","string"]:
            return c
        if self.loop_type == "while":
            if c != "boolean":
                return f"Incompatible types: got '{c}' expected 'boolean': {self.loop_type} {self.cond}"
        elif self.loop_type == "for":
            if c != "integer":
                return f"Incompatible types: got '{c}' expected 'integer': {self.loop_type} {self.assignment} {self.for_type} {self.cond}"

    def generateVmCode(self):
        code = ""
        if self.loop_type == "while":
            code += f"LOOP{self.loopID}:\n"
            code += self.cond.generateVmCode()
            code += f"JZ ENDLOOP{self.loopID}\n"
            code += self.statement.generateVmCode()
            code += f"JUMP LOOP{self.loopID}\n"
            code += f"ENDLOOP{self.loopID}:\n"
        elif self.loop_type == "for":
            global global_vars, func_vars, func_vars_type, local_scope
            if local_scope == "":
                var_pointer = global_vars[self.assignment.id]
                scope = "G"
            else:
                var_pointer = func_vars[local_scope][self.assignment.id]
                scope = "L"
            code += self.assignment.generateVmCode()
            code += f"LOOP{self.loopID}:\n"
            code += f"PUSH{scope} {var_pointer}\n"
            code += self.cond.generateVmCode()
            if self.for_type == "to":
                code += "INFEQ\n"
            elif self.for_type == "downto":
                code += "SUPEQ\n"
            code += f"JZ ENDLOOP{self.loopID}\n"
            code += self.statement.generateVmCode()
            code += f"PUSH{scope} {var_pointer}\n"
            code += "PUSHI 1\n"
            if self.for_type == "to":
                code += "ADD\n"
            elif self.for_type == "downto":
                code += "SUB\n"
            code += f"STORE{scope} {var_pointer}\n"
            code += f"JUMP LOOP{self.loopID}\n"
            code += f"ENDLOOP{self.loopID}:\n"
        return code

    def __str__(self):
        loop = ""
        if self.loop_type == "for":
            loop += f"for {str(self.cond)} do\n"
            for statement in self.statement:
                loop += f"{str(statement)}\n"
        elif self.loop_type == "while":
            loop += f"while {str(self.cond)} do\n"
            for statement in self.statement:
                loop += f"{str(statement)}\n"
        return loop

    __repr__ = __str__

class If(Statement):
    nextID = 0

    def __init__(self, cond, true_statement, false_statement=None):
        self.cond = cond                            # classe Expression
        self.true_statement = true_statement        # classe Statement
        self.false_statement = false_statement      # classe Statement
        self.ifID = If.nextID
        If.nextID += 1
        
    def anasem(self):
        c = self.cond.anasem()
        if c not in ["integer","boolean","real","string"]:
            return c
        elif c != "boolean":
            return f"Incompatible types: got '{c}' expected 'boolean': if {self.cond}"
    
    def generateVmCode(self):
        code = ""
        code += self.cond.generateVmCode()
        if self.false_statement != None:
            code += f"JZ ELSE{self.ifID} // if\n"
        else:
            code += f"JZ ENDIF{self.ifID} // if\n"
        code += self.true_statement.generateVmCode()
        code += f"JUMP ENDIF{self.ifID}\n"
        if self.false_statement != None:
            code += f"ELSE{self.ifID}: // else\n"
            code += self.false_statement.generateVmCode()
            code += f"JUMP ENDIF{self.ifID}\n"
        code += f"ENDIF{self.ifID}:\n"
        return code

    def __str__(self):
        if_statement = f"if {str(self.cond)} then\n"
        for statement in self.true_statement:
            if_statement += f"{str(statement)}\n"
        if self.false_statement:
            if_statement += "else\n"
            for i, statement in enumerate(self.false_statement):
                if_statement += f"{str(statement)}"
                if i != len(self.false_statement)-1:
                    if_statement += "\n"
        if_statement += ";"
        return if_statement

    __repr__ = __str__

class CodeBlock(Statement):
    def __init__(self, algorithm):
        self.algorithm = algorithm      # classe Algorithm
        
    def anasem(self):
        return self.algorithm.anasem()

    def generateVmCode(self):
        code = ""
        code += f"{self.algorithm.generateVmCode()}"
        return code

    def __str__(self):
        code = f"begin\n"
        code += f"{str(self.algorithm)}"
        code += f"end"
        return code

    __repr__ = __str__

class Expression:
    pass

class BinaryOp(Expression):
    def __init__(self, left, op, right):
        self.left = left        # classe Expression
        self.op = op            # string operador
        self.right = right      # classe Expression
    
    def anasem(self):
        code = ""
        if self.op == "+":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'real'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "-":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'real'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "OR":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "boolean" and r == 'boolean':
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'boolean', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "*":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'real'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "/":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'real'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "AND":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "boolean" and r == 'boolean':
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'boolean', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "MOD":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "DIV":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == "integer" and r == 'integer':
                return 'integer'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "=":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == r:
                return "boolean"
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of the same type, but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "<>":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l == r:
                return "boolean"
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of the same type, but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "<":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == "<=":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == ">":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"
        elif self.op == ">=":
            l = self.left.anasem()
            r = self.right.anasem()
            if l[0] == "procedure":
                return f"Cannot use procedure {l[1]} as a value: {self.left} {self.op} {self.right}"
            if r[0] == "procedure":
                return f"Cannot use procedure {r[1]} as a value: {self.left} {self.op} {self.right}"
            if l not in ["integer","boolean","real","string"]:
                return l
            elif r not in ["integer","boolean","real","string"]:
                return r
            elif l in ["integer","real"] and r in ['integer','real']:
                return 'boolean'
            else:
                return f"Incompatible types: Operator '{self.op}' expects operands of type 'integer' or 'real', but got '{l}' and '{r}': {self.left} {self.op} {self.right}"

    def generateVmCode(self):
        code = ""
        if self.op == "+":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "ADD\n"
        elif self.op == "-":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "SUB\n"
        elif self.op == "OR":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "OR\n"
        elif self.op == "*":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "MUL\n"
        elif self.op == "/":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "DIV\n"
        elif self.op == "AND":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "AND\n"
        elif self.op == "MOD":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "MOD\n"
        elif self.op == "DIV":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "DIV\n"
        elif self.op == "=":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "EQUAL\n"
        elif self.op == "<>":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "EQUAL\n"
            code += "NOT\n"
        elif self.op == "<":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "INF\n"
        elif self.op == "<=":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "INFEQ\n"
        elif self.op == ">":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "SUP\n"
        elif self.op == ">=":
            code += self.left.generateVmCode()
            code += self.right.generateVmCode()
            code += "SUPEQ\n"
        return code

    def __str__(self):
        bin_op = f"{str(self.left)} {self.op} {str(self.right)}"
        return bin_op

    __repr__ = __str__

class UnaryOp(Expression):
    def __init__(self, op, expr):
        self.op = op        # string operador
        self.expr = expr    # classe Expression
    
    def anasem(self):
        var_type = self.expr.anasem()
        if var_type == "boolean":
            return "boolean"
        elif var_type not in ["integer","boolean","real","string"]:
            return var_type
        else:
            return f"Incompatible types: Operator '{self.op}' expects operand of type 'boolean', but got '{var_type}': {self.op} {self.expr}"

    def generateVmCode(self):
        code = ""
        if self.op == "NOT":
            code += self.expr.generateVmCode()
            code += "NOT\n"
        return code

    def __str__(self):
        unary_op = f"{self.op} {str(self.expr)}"
        return unary_op

    __repr__ = __str__

class Value(Expression):
    def __init__(self, value, type, array_pos=None, pos_type=None):
        self.value = value      # valor
        self.type = type        # string do tipo do valor
        self.array_pos = array_pos
        self.pos_type = pos_type
    
    def anasem(self):
        if self.type == "int":
            return "integer"
        elif self.type == "real":
            return "real"
        elif self.type == "string":
            return "string"
        elif self.type == "bool":
            return "boolean"
        elif self.type == "id":
            if (self.value in global_vars_type.keys()):
                return global_vars_type[self.value]
            else:
                return f"This variable was not declared before: '{self.value}'"

    def generateVmCode(self):
        code = ""
        global global_vars, global_vars_type, array_init, func_vars, func_vars_type, local_scope
        if local_scope == "":
            scope = "G"
        else:
            scope = "L"
        if self.type == "int":
            code += f"PUSHI {int(self.value)}\n"
        elif self.type == "real":
            code += f"PUSHF {float(self.value)}\n"
        elif self.type == "string":
            value = str(self.value).replace("'", '"')
            code += f"PUSHS {str(value)}\n"
            if len(value) == 3:
                code += "CHRCODE\n"
        elif self.type == "bool":
            code += f"PUSHI {int(self.value)}\n"
        elif self.type == "id":

            if local_scope == "":
                var_pointer = global_vars[str(self.value)]
                scope = "G"
            else:
                var_pointer = func_vars[local_scope][str(self.value)]
                scope = "L"
            code += f"PUSH{scope} {var_pointer}\n"

        elif self.type == "array":
            if local_scope == "":
                var_pointer = global_vars[str(self.value)]
                var_type = global_vars_type[str(self.value)]
            else:
                var_pointer = func_vars[local_scope][str(self.value)]
                var_type = func_vars_type[local_scope][str(self.value)]
            if var_type == "string":
                code += f"PUSH{scope} {var_pointer}\n"
                pos = f"PUSHI {self.array_pos}\n"
                if self.pos_type == "id":
                    if local_scope == "":
                        id_pointer = global_vars[str(self.array_pos)]
                        scope = "G"
                    else:
                        id_pointer = func_vars[local_scope][str(self.array_pos)]
                        scope = "L"
                    pos = f"PUSH{scope} {id_pointer}\n"
                code += pos
                code += f"PUSHI 1\n"
                code += "SUB\n"
                code += "CHARAT\n"
            else:
                init = array_init[self.value]
                code += f"PUSH{scope} {var_pointer}\n"
                pos = f"PUSHI {self.array_pos}\n"
                if self.pos_type == "id":
                    id_pointer = global_vars[str(self.array_pos)]
                    pos = f"PUSH{scope} {id_pointer}\n"
                code += pos
                code += f"PUSHI {init}\n"
                code += "SUB\n"
                code += "LOADN\n"

        return code

    def generateVmCodeArray(self):
        code = ""
        global global_vars, global_vars_type, array_init, func_vars, func_vars_type, local_scope
        if self.type == "array":
            if local_scope == "":
                var_pointer = global_vars[str(self.value)]
                scope = "G"
            else:
                var_pointer = func_vars[local_scope][str(self.value)]
                scope = "L"
            init = array_init[self.value]
            code += f"PUSH{scope} {var_pointer}\n"
            pos = f"PUSHI {self.array_pos}\n"
            if self.pos_type == "id":
                if local_scope == "":
                    id_pointer = global_vars[str(self.array_pos)]
                else:
                    id_pointer = func_vars[local_scope][str(self.array_pos)]
                pos = f"PUSH{scope} {id_pointer}\n"
            code += pos
            code += f"PUSHI {init}\n"
            code += "SUB\n"
        return code

    def __str__(self):
        return str(self.value)

    __repr__ = __str__

class FunctionCall(Expression):
    def __init__(self, id, args):
        self.id = str(id).lower()   # ID da função
        self.args = args            # lista de argumentos da função classes Value ou FunctionCall  ########  Ver como distinguir se os argumentos são variáveis ou só valores
        
    def anasem(self):
        if self.id == "writeln" or self.id == "write":
            return ("procedure",self.id)
        elif self.id == "readln":
            return ("procedure",self.id)
        
    def generateVmCode(self):
        code = ""
        global global_vars, global_vars_type, array_type, func_vars, func_vars_type, local_scope
        if self.id == "writeln" or self.id == "write":
            for arg in self.args:
                try:
                    if local_scope == "":
                        var_pointer = global_vars[str(arg)]
                        var_type = global_vars_type[str(arg)]
                    else:
                        var_pointer = func_vars[local_scope][str(arg)]
                        var_type = func_vars_type[local_scope][str(arg)]
                except:
                    var_pointer = None
                    var_type = None
                if var_type == "string":
                    code += arg.generateVmCode()
                    if len(str(arg.value)) == 3:
                        code += "WRITECHR\n"
                    else:
                        code += "WRITES\n"
                elif var_type == "integer":
                    code += arg.generateVmCode()
                    code += f"WRITEI\n"
                elif var_type == "real":
                    code += arg.generateVmCode()
                    code += f"WRITEF\n"
                elif var_type == "boolean":
                    code += arg.generateVmCode()
                    code += f"WRITEI\n"
                elif isinstance(arg, BinaryOp):
                    code += arg.generateVmCode()
                    code += f"WRITEI\n"
                elif var_type == "array":
                    type_array = array_type[str(arg)]
                    if type_array == "string":
                        code += arg.generateVmCode()
                        code += "WRITES\n"
                    elif type_array == "integer":
                        code += arg.generateVmCode()
                        code += f"WRITEI\n"
                    elif type_array == "real":
                        code += arg.generateVmCode()
                        code += f"WRITEF\n"
                    elif type_array == "boolean":
                        code += arg.generateVmCode()
                        code += f"WRITEI\n"
                else:
                    arg = str(arg).replace("'", '"')
                    code += f"PUSHS {arg}\n"
                    code += "WRITES\n"
            if self.id == "writeln":
                code += "WRITELN\n"
        elif self.id == "readln":
            try:
                if local_scope == "":
                    var_pointer = global_vars[str(self.args[0])]
                    var_type = global_vars_type[str(self.args[0])]
                    scope = "G"
                else:
                    var_pointer = func_vars[local_scope][str(self.args[0])]
                    var_type = func_vars_type[local_scope][str(self.args[0])]
                    scope = "L"
            except:
                var_pointer = None
                var_type = None
            is_array = False
            if var_type == "array":
                var_type = array_type[str(self.args[0])]
                code += self.args[0].generateVmCodeArray()
                is_array = True
            code += "READ\n"
            if var_type == "integer":
                code += f"ATOI\n"
            elif var_type == "real":
                code += f"ATOF\n"
            elif var_type == "boolean":
                code += f"ATOI\n"
            if is_array:
                code += "STOREN\n"
            else:
                code += f"STORE{scope} {var_pointer}\n"
        elif self.id == "length":
            if local_scope == "":
                var_pointer = global_vars[str(self.args[0])]
                var_type = global_vars_type[str(self.args[0])]
                scope = "G"
            else:
                var_pointer = func_vars[local_scope][str(self.args[0])]
                var_type = func_vars_type[local_scope][str(self.args[0])]
                scope = "L"
            if var_type == "string":
                code += f"PUSH{scope} {var_pointer}\n"
                code += f"STRLEN\n"
        else:
            global known_functions, func_vars_number
            if str(self.id).lower() in known_functions.keys():
                func_pos = known_functions[str(self.id).lower()]
                number_vars = func_vars_number[str(self.id).lower()]
                for arg in self.args:
                    code += arg.generateVmCode()
                code += f"PUSHA {self.id}\n"
                code += "CALL\n"
                if func_pos == -1:
                    code += f"POP {len(self.args) + number_vars}\n"
                else:
                    code += f"POP {len(self.args) + number_vars}\n"
                    code += f"PUSHG {func_pos}\n"
        return code

    def __str__(self):
        func_call = f"{self.id}("
        for i, arg in enumerate(self.args):
            if i != 0:
                func_call += ", "
            func_call += f"{str(arg)}"
        func_call += ")"
        return func_call

    __repr__ = __str__
