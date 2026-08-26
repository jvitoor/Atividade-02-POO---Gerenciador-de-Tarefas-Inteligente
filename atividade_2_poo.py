from enum import Enum
from datetime import datetime, date

class Prioridade(Enum):
    BAIXA = 1; MEDIA = 2; ALTA = 3; URGENTE = 4

class Status(Enum):
    PENDENTE = 1; EM_ANDAMENTO = 2; CONCLUIDA = 3

class Tarefa:
    def __init__(self, titulo: str, descricao: str, prioridade: Prioridade, dataLimite: date, projeto):
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.dataLimite = dataLimite
        self.status = Status.PENDENTE
        self.projeto = projeto

    def marcarConcluida(self):
        self.status = Status.CONCLUIDA

    def estaVencida(self):
        return date.today() > self.dataLimite

class Projeto:
    def __init__(self, nome: str, descricao: str, usuario):
        self.nome = nome
        self.descricao = descricao
        self.usuario = usuario
        self.tarefas = []

    def adicionarTarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)

    def removerTarefa(self, tarefa: Tarefa):
        if tarefa in self.tarefas:
            self.tarefas.remove(tarefa)

    def calcularProgresso(self) -> float:
        if not self.tarefas: return 0.0
        concluidas = sum(1 for t in self.tarefas if t.status == Status.CONCLUIDA)
        return (concluidas / len(self.tarefas)) * 100

class Usuario:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
        self.projetos = []

    def criarProjeto(self, nome: str, descricao: str) -> Projeto:
        projeto = Projeto(nome, descricao, self)
        self.projetos.append(projeto)
        return projeto
    
    def removerProjeto(self, projeto: Projeto):
        if projeto in self.projetos:
            self.projetos.remove(projeto)

class SistemaDeTarefas:
    def __init__(self):
        self.usuarios = []
        
    def adicionarUsuario(self, usuario: Usuario):
        self.usuarios.append(usuario)
        
    def removerUsuario(self, usuario: Usuario):
        if usuario in self.usuarios:
            self.usuarios.remove(usuario)

    def relatorios(self):
        print("\n--- RELATÓRIO GERAL ---")
        if not self.usuarios:
            print("Nenhum dado cadastrado no sistema.")
            return
            
        for u in self.usuarios:
            print(f"\nUsuário: {u.nome}")
            for p in u.projetos:
                print(f"  Projeto: {p.nome} ({p.calcularProgresso():.1f}% Concluído)")
                for t in p.tarefas:
                    vencida = " (VENCIDA)" if t.estaVencida() and t.status != Status.CONCLUIDA else ""
                    print(f"   - [{t.status.name}] {t.titulo} (Prioridade: {t.prioridade.name}){vencida}")


# Menu

def menu():
    sistema = SistemaDeTarefas()
    usuario_atual = None
    projeto_atual = None

    while True:
        print("\nGerenciador Inteligente de Tarefas")
        print(f"Usuário Logado: {usuario_atual.nome if usuario_atual else 'Nenhum'}")
        print(f"Projeto Atual: {projeto_atual.nome if projeto_atual else 'Nenhum'}")
        print("-" * 40)
        print("1 - Cadastrar Usuário")
        print("2 - Remover Usuário")
        print("3 - Criar Projeto")
        print("4 - Remover Projeto")
        print("5 - Adicionar Tarefa")
        print("6 - Concluir Tarefa")
        print("7 - Exibir Relatórios")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do usuário: ")
            email = input("E-mail: ")
            usuario_atual = Usuario(nome, email)
            sistema.adicionarUsuario(usuario_atual)
            print(f"Usuário '{nome}' cadastrado e logado com sucesso!")

        elif opcao == '2':
            if not sistema.usuarios:
                print("Não há usuários cadastrados no sistema.")
                continue
            print("\nUsuários cadastrados:")
            for i, u in enumerate(sistema.usuarios):
                print(f"{i} - {u.nome} ({u.email})")
            
            try:
                idx = int(input("Digite o número do usuário que deseja remover: "))
                usuario_remover = sistema.usuarios[idx]
                sistema.removerUsuario(usuario_remover)
                
                # Se excluiu o usuário que estava logado, desloga ele
                if usuario_atual == usuario_remover:
                    usuario_atual = None
                    projeto_atual = None
                print("Usuário removido com sucesso!")
            except (IndexError, ValueError):
                print("Opção inválida!")

        elif opcao == '3':
            if not usuario_atual:
                print("Cadastre ou selecione um usuário primeiro!")
                continue
            nome_proj = input("Nome do projeto: ")
            desc_proj = input("Descrição: ")
            projeto_atual = usuario_atual.criarProjeto(nome_proj, desc_proj)
            print("Projeto criado com sucesso!")

        elif opcao == '4':
            if not usuario_atual or not usuario_atual.projetos:
                print("Não há projetos para o usuário atual.")
                continue
            print("\nProjetos de", usuario_atual.nome, ":")
            for i, p in enumerate(usuario_atual.projetos):
                print(f"{i} - {p.nome}")
            
            try:
                idx = int(input("Digite o número do projeto que deseja remover: "))
                projeto_remover = usuario_atual.projetos[idx]
                usuario_atual.removerProjeto(projeto_remover)
                
                # Se excluiu o projeto selecionado, remove a seleção
                if projeto_atual == projeto_remover:
                    projeto_atual = None
                print("Projeto removido com sucesso!")
            except (IndexError, ValueError):
                print("Opção inválida!")

        elif opcao == '5':
            if not projeto_atual:
                print("Crie um projeto primeiro!")
                continue
            titulo = input("Título da tarefa: ")
            desc = input("Descrição: ")
            print("Prioridades: 1-Baixa, 2-Média, 3-Alta, 4-Urgente")
            
            try:
                pri_op = int(input("Escolha a prioridade (1 a 4): "))
                data_str = input("Data limite (DD/MM/AAAA): ")
                data_limite = datetime.strptime(data_str, "%d/%m/%Y").date()
                
                tarefa = Tarefa(titulo, desc, Prioridade(pri_op), data_limite, projeto_atual)
                projeto_atual.adicionarTarefa(tarefa)
                print("Tarefa adicionada!")
            except ValueError:
                print("Data ou prioridade em formato inválido! Tente novamente.")

        elif opcao == '6':
            if not projeto_atual or not projeto_atual.tarefas:
                print("Nenhuma tarefa encontrada neste projeto!")
                continue
            print("\nTarefas do projeto", projeto_atual.nome, ":")
            for i, t in enumerate(projeto_atual.tarefas):
                print(f"{i} - {t.titulo} [{t.status.name}]")
            
            try:
                idx = int(input("Digite o número da tarefa para concluir: "))
                projeto_atual.tarefas[idx].marcarConcluida()
                print("Tarefa concluída!")
            except (IndexError, ValueError):
                print("Opção inválida!")

        elif opcao == '7':
            sistema.relatorios()

        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
