import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


# ======== CLASSES BÁSICAS ========

class Competencia:
    def __init__(self, nome, tipo, nivel=0):
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel


class Perfil:
    def __init__(self, nome):
        self.nome = nome
        self.competencias = []


class Carreira:
    def __init__(self, nome, exigencias, pesos):
        self.nome = nome
        self.exigencias = exigencias
        self.pesos = pesos

    def calcular(self, perfil):
        total, peso_total = 0, 0
        for nome, exig in self.exigencias.items():
            comp = next((c for c in perfil.competencias if c.nome == nome), None)
            peso = self.pesos.get(nome, 1)
            if not comp:
                continue
            nota = 10 if comp.nivel >= exig else (comp.nivel / exig) * 10
            total += nota * peso
            peso_total += peso
        return round((total / (10 * peso_total)) * 100, 1) if peso_total else 0


# ======== APP ========

class SistemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analista de carreiras")
        self.root.geometry("500x600")
        self.root.configure(bg="#f8f9fa")

        self.arquivo_dados = "perfis.json"
        self.perfis = self.carregar_perfis()
        self.carreiras = []
        self.criar_carreiras()

        self.nome_var = tk.StringVar()
        self.inputs = {}

        self.monta_interface()

    # ======== DADOS ========
    def criar_carreiras(self):
        self.carreiras = [
            Carreira("Desenvolvedor de Software",
                     {"logica": 8, "criatividade": 6, "colaboracao": 5, "adaptabilidade": 7},
                     {"logica": 3, "criatividade": 2, "colaboracao": 1, "adaptabilidade": 2}),
            Carreira("Designer UX/UI",
                     {"logica": 5, "criatividade": 9, "colaboracao": 7, "adaptabilidade": 6},
                     {"logica": 1, "criatividade": 3, "colaboracao": 2, "adaptabilidade": 2}),
            Carreira("Analista de Dados",
                     {"logica": 9, "criatividade": 5, "colaboracao": 6, "adaptabilidade": 7},
                     {"logica": 4, "criatividade": 1, "colaboracao": 2, "adaptabilidade": 2}),
            Carreira("Gerente de Projetos",
                     {"logica": 6, "criatividade": 6, "colaboracao": 9, "adaptabilidade": 8},
                     {"logica": 1, "criatividade": 1, "colaboracao": 4, "adaptabilidade": 3})
        ]

    # ======== INTERFACE ========
    def monta_interface(self):
        tk.Label(self.root, text="Analista de carreiras", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333").pack(pady=12)

        # Nome
        nome_frame = tk.Frame(self.root, bg="#f8f9fa")
        nome_frame.pack()
        tk.Label(nome_frame, text="Nome do Perfil:", bg="#f8f9fa").pack(side="left", padx=5)
        tk.Entry(nome_frame, textvariable=self.nome_var, width=25, justify="center").pack(side="left", padx=5)

        # Competências
        comp_frame = tk.LabelFrame(self.root, text="Competências (0-10)", bg="#f8f9fa", padx=10, pady=10)
        comp_frame.pack(pady=15, padx=15, fill="x")

        competencias = ["logica", "criatividade", "colaboracao", "adaptabilidade"]
        for c in competencias:
            frame = tk.Frame(comp_frame, bg="#f8f9fa")
            frame.pack(pady=4)
            tk.Label(frame, text=f"{c.capitalize()}:", width=15, anchor="w", bg="#f8f9fa").pack(side="left")
            var = tk.StringVar()
            self.inputs[c] = var
            tk.Entry(frame, textvariable=var, width=6, justify="center").pack(side="left")

        # Botões
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Cadastrar Perfil", command=self.salvar_perfil, bg="#d1e7dd", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Analisar Perfil", command=self.analisar, bg="#cfe2ff", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Excluir Perfil", command=self.excluir_perfil, bg="#ffe5b4", width=15).grid(row=0, column=2, padx=5)

        # Lista de perfis
        tk.Label(self.root, text="Perfis Salvos:", bg="#f8f9fa").pack()
        self.lista_perfis = ttk.Combobox(self.root, state="readonly", values=[p.nome for p in self.perfis], width=30)
        self.lista_perfis.pack(pady=5)
        self.lista_perfis.bind("<<ComboboxSelected>>", self.selecionar_perfil)

        # Barra de progresso
        self.progress_label = tk.Label(self.root, text="", bg="#f8f9fa")
        self.progress_label.pack()
        self.progress = ttk.Progressbar(self.root, length=400, mode="determinate")
        self.progress.pack(pady=5)

        # Resultado
        result_frame = tk.Frame(self.root, bg="#f8f9fa")
        result_frame.pack(pady=10, fill="both", expand=True)

        self.result_text = tk.Text(result_frame, wrap="word", height=10, width=55, bg="#ffffff", relief="solid")
        self.result_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        scroll.pack(side="right", fill="y")
        self.result_text.configure(yscrollcommand=scroll.set)

    # ======== FUNÇÕES DE PERFIS ========
    def salvar_perfil(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Coloca o nome do perfil, pô!")
            return

        p = Perfil(nome)
        for c, var in self.inputs.items():
            try:
                n = int(var.get())
                if not (0 <= n <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", f"Valor inválido para {c}. Use de 0 a 10.")
                return
            tipo = "tecnica" if c == "logica" else "comportamental"
            p.competencias.append(Competencia(c, tipo, n))

        # Substitui se já existir
        self.perfis = [p for p in self.perfis if p.nome != nome]
        self.perfis.append(p)
        self.salvar_em_arquivo()

        messagebox.showinfo("Sucesso", f"Perfil '{nome}' salvo com sucesso!")
        self.lista_perfis["values"] = [p.nome for p in self.perfis]
        self.nome_var.set("")
        for v in self.inputs.values():
            v.set("")

    def excluir_perfil(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do perfil a excluir.")
            return
        self.perfis = [p for p in self.perfis if p.nome != nome]
        self.salvar_em_arquivo()
        self.lista_perfis["values"] = [p.nome for p in self.perfis]
        messagebox.showinfo("Excluído", f"Perfil '{nome}' removido com sucesso!")
        self.result_text.delete("1.0", tk.END)
        self.progress["value"] = 0
        self.progress_label.config(text="")

    def selecionar_perfil(self, event=None):
        nome = self.lista_perfis.get()
        if nome:
            self.nome_var.set(nome)

    def analisar(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Escolha ou digite um perfil para analisar.")
            return

        perfil = next((p for p in self.perfis if p.nome == nome), None)
        if not perfil:
            messagebox.showwarning("Aviso", "Perfil não encontrado.")
            return

        resultados = [(c.nome, c.calcular(perfil)) for c in self.carreiras]
        resultados.sort(key=lambda x: x[1], reverse=True)

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"📋 Perfil: {perfil.nome}\n\n")

        media = sum(pct for _, pct in resultados) / len(resultados)
        for nome, pct in resultados:
            emoji = "🚀" if pct >= 80 else "⚙️" if pct >= 60 else "🧩"
            self.result_text.insert(tk.END, f"{emoji} {nome}: {pct}% compatível\n")

        self.progress["value"] = media
        self.progress_label.config(text=f"Compatibilidade média: {round(media, 1)}%")

    # ======== SALVAR E CARREGAR ========
    def salvar_em_arquivo(self):
        dados = []
        for p in self.perfis:
            dados.append({
                "nome": p.nome,
                "competencias": [{"nome": c.nome, "tipo": c.tipo, "nivel": c.nivel} for c in p.competencias]
            })
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar_perfis(self):
        if not os.path.exists("perfis.json"):
            return []
        with open("perfis.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        perfis = []
        for p in dados:
            perfil = Perfil(p["nome"])
            for c in p["competencias"]:
                perfil.competencias.append(Competencia(c["nome"], c["tipo"], c["nivel"]))
            perfis.append(perfil)
        return perfis


# ======== MAIN ========
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaApp(root)
    root.mainloop()