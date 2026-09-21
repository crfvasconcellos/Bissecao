import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

def metodo_bissecao(f, a, b, n_exp=1, max_iter=100):
    epsilon = 10**(-n_exp)
    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        return None, None, "Erro: f(a) e f(b) devem ter sinais opostos!"

    tabela = []
    x_ant = (a + b) / 2.0
    fx0 = f(x_ant)
    tabela.append((0, a, b, x_ant, fx0, None))

    if fx0 == 0:
        return x_ant, tabela, f"x_0 = {x_ant:.5f} é a raíz exata!"

    if fa * fx0 < 0:
        b = x_ant
    else:
        a = x_ant
        fa = fx0

    raiz = x_ant
    msg_final = ""

    for n in range(1, max_iter + 1):
        x_atual = (a + b) / 2.0
        fx = f(x_atual)
        erro = abs(x_atual - x_ant)
        tabela.append((n, a, b, x_atual, fx, erro))

        if fx == 0:
            raiz = x_atual
            msg_final = f"x_{n} = {x_atual:.5f} é a raíz exata!"
            break

        if erro < epsilon:
            raiz = x_atual
            msg_final = f"A raíz aproximada é x_{n} = {x_atual:.5f}"
            break

        if fa * fx < 0:
            b = x_atual
        else:
            a = x_atual
            fa = fx

        x_ant = x_atual

    return raiz, tabela, msg_final

class AppBissecao:
    def __init__(self, root):
        self.root = root
        self.root.title("Método da Bisseção")
        self.root.geometry("620x540")
        self.root.resizable(False, False)

        self.dados_grafico = None

        frame_inputs = ttk.LabelFrame(root, text=" Parâmetros de Entrada ")
        frame_inputs.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_inputs, text="Função f(x):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_func = ttk.Entry(frame_inputs, width=20)
        self.ent_func.insert(0, "x**2 - 3")
        self.ent_func.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Intervalo [a]:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_a = ttk.Entry(frame_inputs, width=8)
        self.ent_a.insert(0, "1.0")
        self.ent_a.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Intervalo [b]:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_b = ttk.Entry(frame_inputs, width=20)
        self.ent_b.insert(0, "2.0")
        self.ent_b.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Tolerância n (10^-n):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ent_n = ttk.Entry(frame_inputs, width=8)
        self.ent_n.insert(0, "1")
        self.ent_n.grid(row=1, column=3, padx=5, pady=5)

        self.btn_calc = ttk.Button(frame_inputs, text="Calcular", command=self.calcular)
        self.btn_calc.grid(row=2, column=0, columnspan=4, pady=8)

        frame_tabela = ttk.LabelFrame(root, text=" Tabela de Iterações ")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("n", "a_n", "b_n", "x_n", "f(x_n)", "epsilon")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=95, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        frame_rodape = ttk.Frame(root)
        frame_rodape.pack(fill="x", padx=10, pady=5)

        self.lbl_resultado = ttk.Label(frame_rodape, text="", font=("Arial", 10, "bold"), foreground="blue")
        self.lbl_resultado.pack(side="left", padx=5)

        self.btn_grafico = ttk.Button(frame_rodape, text="Ver Gráfico", state="disabled", command=self.exibir_grafico)
        self.btn_grafico.pack(side="right", padx=5)

    def calcular(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        expr = self.ent_func.get()
        try:
            f = lambda x: eval(expr, {"x": x, "math": math, "np": math})
            a = float(self.ent_a.get())
            b = float(self.ent_b.get())
            n_exp = int(self.ent_n.get())
        except Exception:
            messagebox.showerror("Erro", "Verifique os valores digitados!")
            return

        raiz, tabela, msg = metodo_bissecao(f, a, b, n_exp)

        if tabela is None:
            messagebox.showerror("Erro de Sinais", msg)
            self.btn_grafico.config(state="disabled")
            return

        for linha in tabela:
            n, an, bn, xn, fxn, err = linha
            err_str = f"{err:.5f}" if err is not None else "---"
            self.tree.insert("", "end", values=(n, f"{an:.5f}", f"{bn:.5f}", f"{xn:.5f}", f"{fxn:.5f}", err_str))

        self.lbl_resultado.config(text=msg)
        self.dados_grafico = (f, a, b, tabela, raiz)
        self.btn_grafico.config(state="normal")

    def exibir_grafico(self):
        if not self.dados_grafico:
            return
        f, a, b, tabela, raiz = self.dados_grafico

        passos = 300
        x_min, x_max = a - 0.2, b + 0.2
        x_vals = [x_min + i * (x_max - x_min) / passos for i in range(passos + 1)]
        y_vals = [f(x) for x in x_vals]

        plt.figure(figsize=(7, 4))
        plt.plot(x_vals, y_vals, label="f(x)", color="blue")
        plt.axhline(0, color="black", linestyle="--", linewidth=0.8)

        xs = [linha[3] for linha in tabela]
        ys = [linha[4] for linha in tabela]
        plt.scatter(xs[:-1], ys[:-1], color="orange", s=35, label="Iterações")
        plt.scatter([raiz], [f(raiz)], color="red", marker="*", s=140, zorder=5, label=f"Raiz: {raiz:.5f}")

        plt.title("Método da Bisseção")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True, linestyle=":")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    janela = tk.Tk()
    app = AppBissecao(janela)
    janela.mainloop()