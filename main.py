import math

def resolver():
    expr = input("Digite a funcao f(x): ")
    f = lambda x: eval(expr, {"x": x, "math": math, "np": math})
    
    a = float(input("Digite o inicio do intervalo (a): "))
    b = float(input("Digite o fim do intervalo (b): "))
    n_exp = int(input("Digite o n da tolerancia (10^-n): "))
    
    epsilon = 10**(-n_exp)
    
    if f(a) * f(b) >= 0:
        print("\nErro: f(a) e f(b) devem ter sinais opostos!")
        return

    x_ant = (a + b) / 2.0
    fx0 = f(x_ant)
    
    print("\n" + f"{'n':^3} | {'a_n':^9} | {'b_n':^9} | {'x_n':^9} | {'f(x_n)':^10} | {'epsilon':^9}")
    print("-" * 59)
    print(f"{0:^3} | {a:^9.5f} | {b:^9.5f} | {x_ant:^9.5f} | {fx0:^10.5f} | {'---':^9}")

    if fx0 == 0:
        print(f"\nx_0 = {x_ant:.5f} é a raíz exata")
        return

    if f(a) * fx0 < 0:
        b = x_ant
    else:
        a = x_ant

    raiz = x_ant

    for n in range(1, 100):
        x_atual = (a + b) / 2.0
        fx = f(x_atual)
        erro = abs(x_atual - x_ant)
        
        print(f"{n:^3} | {a:^9.5f} | {b:^9.5f} | {x_atual:^9.5f} | {fx:^10.5f} | {erro:^9.5f}")

        if fx == 0:
            print(f"\nx_{n} = {x_atual:.5f} é a raíz exata")
            raiz = x_atual
            break

        if erro < epsilon:
            print(f"\nA raíz aproximada é x_{n} = {x_atual:.5f}")
            raiz = x_atual
            break

        if f(a) * fx < 0:
            b = x_atual
        else:
            a = x_atual

        x_ant = x_atual

if __name__ == "__main__":
    resolver()