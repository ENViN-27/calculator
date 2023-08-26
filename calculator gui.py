from tkinter import *

class Node:
    def __init__(self, val=None):
        self.val = val
        self.next = None

class Stack:
    def __init__(self):
        self.head = Node()
        self.size = 0
        
    def getsize(self): return self.size

    def isempty(self): return (self.size==0)

    def top(self): return (None if self.isempty() else self.head.val)

    def push(self, val):
        new = Node(val)
        new.next = self.head
        self.head = new
        self.size += 1
    
    def pop(self):
        if self.isempty():
            return None
        val = self.head.val
        self.head = self.head.next
        self.size -= 1
        return val

class Expression():
    def __init__(self,exp=[]):
        self.exp = exp
        self.size = len(exp)
        self.stack = Stack()

    def show(self): return "".join(self.exp)

    def isOperator(self, e): return (True if e in ("+","-","*","/","^") else False)

    def isOperand(self, e): return (True if e.isalnum() else False)

    def push(self, e):
        if self.size > 0:
            top = self.exp[-1]
            # if self.isOperand(top) and e == ".":

            if self.isOperand(top) and (self.isOperand(e) or e=="."):
                self.exp[-1] += e
                return 2
            elif self.isOperator(top) and self.isOperator(e):
                self.exp[-1] = e
                return 0
            else:
                self.exp.append(e)
                self.size += 1
                return 1
        else:
            if self.isOperand(e):
                self.exp.append(e)
                self.size += 1
                return 1
            else:
                return 0
    def pop(self):
        if self.size == 0:
            return None
        top = self.exp[-1]
        self.size -= 1
        self.exp = self.exp[0:self.size]
        return top
    def clr(self):
        self.exp = []
        self.size = 0

    # Check if the operator "s" at the top of stack has lower precedence than "e" or not.
    def checkPrecedence(self, s, e): return (True if (e=="^" and s in ["+","-","*","/"]) or (e in ["*","/"] and s in ["+","-"]) else False)

    def infix_to_postfix(self):
        postfix = []
        for e in self.exp:
            if self.isOperand(e):
                postfix.append(e) # add to postfix
            elif self.isOperator(e):
                if not (self.stack.top() == "(" or self.checkPrecedence(self.stack.top(),e)):
                    while not self.stack.isempty() and self.stack.top() not in ("(",")") and (not self.checkPrecedence(self.stack.top(),e)):
                        postfix.append(self.stack.pop()) # add to postfix
                self.stack.push(e)
            elif e == "(":
                self.stack.push(e)
            elif e == ")":
                while not self.stack.isempty() and self.stack.top() != "(":
                    postfix.append(self.stack.pop()) # add to postfix
                self.stack.pop()
        while not self.stack.isempty():
            postfix.append(self.stack.pop()) # add to postfix
        return postfix
    
    def evaluate(self):
        postfix = Expression(self.exp).infix_to_postfix()
        for e in postfix:
            if self.isOperand(e):
                self.stack.push(int(e))
            else:
                v1 = self.stack.pop()
                v2 = self.stack.pop()
                match e:
                    case "+": self.stack.push(v2+v1)
                    case "-": self.stack.push(v2-v1)
                    case "*": self.stack.push(v2*v1)
                    case "/": self.stack.push(v2/v1)
                    case "^": self.stack.push(v2**v1)
        return self.stack.pop()

# equation = ""
# def show(value):
#     global equation
#     equation += value
#     result_label.config(text=equation)
# def clear():
#     global equation
#     equation = ""
#     result_label.config(text=equation)
# def back():
#     global equation
#     equation = equation[:-1]
#     result_label.config(text=equation)
# def result():
#     global equation
#     try:
#         result_label.config(text=eval(equation))
#         equation = ""
#     except:
#         result_label.config(text="ERROR")
#         equation = ""

def show(exp, value): # Add value to the expression (only if the equation makes sence after adding). Simultaneously update the display value.
    exp.push(value)
    result_label.config(text=exp.show())

def clear(exp): # Set complete expression to empty expression. Simultaneously update the display value.
    exp.clr()
    result_label.config(text='0')

def back(exp): # Remove last element from the expression. Simultaneously update the display value.
    exp.pop()
    result_label.config(text=exp.show())

def result(exp): # Evaluate the expression and update the display value as the result.
    val = exp.evaluate()
    exp.clr()
    # exp.push(str(val))
    result_label.config(text=str(val))


if __name__=="__main__":

    exp = Expression()

    color = {"root":"#242635", "label":"#323548", "text_label":"#f7f7ff", "text_l":"#f7f7ff", "text_d":"#242635",
             "c":"#bdfeea", "x":"#bdfeea", "=":"#bdfeea", "operator":"#323548", "operand":"#323548"}

    root = Tk()
    root.title("Calculator")
    root.configure(bg=color["root"])
    root.geometry("570x600+100+200")
    root.resizable(False,False)

    result_label = Label(root, width=22, height=2, text="0", font=("arial",30,"bold"), anchor="e", justify="right", fg=color["text_label"], bg=color["label"])
    result_label.pack()

    Button(root, text="C", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_d"], bg=color["c"], command=lambda: clear(exp)).place(x=10,y=110)
    Button(root, text="X", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_d"], bg=color["x"], command=lambda:  back(exp)).place(x=150,y=110)
    Button(root, text="=", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_d"], bg=color["="], command=lambda:result(exp)).place(x=430,y=510)

    Button(root, text="^", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operator"], command=lambda:show(exp,"^")).place(x=290,y=110)
    Button(root, text="/", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operator"], command=lambda:show(exp,"/")).place(x=430,y=110)
    Button(root, text="*", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operator"], command=lambda:show(exp,"*")).place(x=430,y=210)
    Button(root, text="-", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operator"], command=lambda:show(exp,"-")).place(x=430,y=310)
    Button(root, text="+", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operator"], command=lambda:show(exp,"+")).place(x=430,y=410)

    Button(root, text="7", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"7")).place(x=10,y=210)
    Button(root, text="8", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"8")).place(x=150,y=210)
    Button(root, text="9", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"9")).place(x=290,y=210)

    Button(root, text="4", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"4")).place(x=10,y=310)
    Button(root, text="6", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"6")).place(x=150,y=310)
    Button(root, text="5", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"5")).place(x=290,y=310)

    Button(root, text="1", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"1")).place(x=10,y=410)
    Button(root, text="2", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"2")).place(x=150,y=410)
    Button(root, text="3", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"3")).place(x=290,y=410)

    Button(root, text="00", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"00")).place(x=10,y=510)
    Button(root, text="0", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,"0")).place(x=150,y=510)
    Button(root, text=".", width=5, height=1, font=("arial",30,"bold"), bd=1, fg=color["text_l"], bg=color["operand"], command=lambda:show(exp,".")).place(x=290,y=510)

    root.mainloop()

    # exp = "a+b*(c^d-e)^(f+g*h)-i"
    # xp = "5+4*(2**4-7)**(1+2*1)-27"
    # print(f"{xp}=",eval(xp))
    # post = expression(exp).infix_to_postfix()
    # print(exp)
    # print(post)
    # print("\n=> infix to postfix:",post=="abcd^e-fgh*+^*+i-","\n")
    
    # exp = expression()
    # while True:
    #     e = input()
    #     match e:
    #         case " ": exp.pop()
    #         case "=": break
    #         case _: exp.push(e)
    # val = exp.evaluate()
    # print(exp.exp,"=",val)

    # exp = ["5","+","4","*","(","2","^","4","-","7",")","^","(","1","+","2","*","1",")","-","27"]
    # exp = ["5","+"]
    # exp = expression(exp)
    # try:
    #     val = exp.evaluate()
    # except:
    #     val = "Error"
    # print(exp.show(),"=",val)