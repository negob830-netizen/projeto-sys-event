import os
from datetime import datetime

# Dicionário global para armazenar os projetos. A chave é o ID do projeto.
projetos = {}
# Tupla de informações do sistema
INFO_SISTEMA = ("ResearchFlow v2.1", "Área Foco: Inteligência Artificial", 2025)
# Contador para gerar IDs únicos para os projetos
ID_CONTADOR = 1

def limpar_terminal():
    """Função auxiliar para limpar o console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def adicionar_projeto():
    """Cria um novo projeto de pesquisa usando o Dicionário."""
    global ID_CONTADOR
    limpar_terminal()
    print("\n--- Iniciar Novo Projeto de Pesquisa ---")
    
    id_novo = ID_CONTADOR
    
    titulo = input("Título do Projeto: ")
    data_limite_str = input("Data Limite (DD/MM/AAAA): ")
    
    try:
        # Validação simples de data
        data_limite = datetime.strptime(data_limite_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        print("[ERRO] Formato de data inválido. Use DD/MM/AAAA. Projeto não adicionado.")
        input("Pressione Enter para continuar...")
        return

    try:
        orcamento = float(input("Orçamento Estimado (R$): "))
    except ValueError:
        print("[ERRO] Orçamento deve ser um número. Projeto não adicionado.")
        input("Pressione Enter para continuar...")
        return

    # Uso de Set para armazenar as áreas de conhecimento
    areas_str = input("Áreas de Conhecimento (separadas por vírgula): ")
    areas_set = set(area.strip().upper() for area in areas_str.split(','))

    novo_projeto = {
        "titulo": titulo,
        "data_limite": data_limite,
        "orcamento": orcamento,
        "status": "PENDENTE", # Status inicial
        "areas": areas_set,
        "membros": [] # Lista de dicionários de membros da equipe
    }
    
    projetos[id_novo] = novo_projeto
    ID_CONTADOR += 1
    print(f"\n[SUCESSO] Projeto '{titulo}' iniciado com ID: {id_novo}.")
    input("Pressione Enter para continuar...")


def listar_projetos():
    """Percorre todos os projetos e os exibe."""
    limpar_terminal()
    print("\n--- Lista de Projetos de Pesquisa ---")
    if not projetos:
        print("Nenhum projeto cadastrado.")
        input("Pressione Enter para continuar...")
        return

    for id_projeto, dados in projetos.items():
        print(f"ID: {id_projeto} | Título: {dados['titulo']} | Data Limite: {dados['data_limite']} | Status: {dados['status']} | Membros: {len(dados['membros'])}")
    
    print("-" * 70)
    input("Pressione Enter para continuar...")


def detalhar_projeto(id_projeto):
    """Recebe o ID do projeto e exibe seus detalhes (incluindo as áreas de conhecimento do Set)."""
    limpar_terminal()
    try:
        dados = projetos[id_projeto]
    except KeyError:
        print(f"\n[ERRO] Projeto com ID {id_projeto} não encontrado.")
        input("Pressione Enter para continuar...")
        return

    print(f"\n--- Detalhes do Projeto ID: {id_projeto} ---")
    print(f"Título: {dados['titulo']}")
    print(f"Data Limite: {dados['data_limite']}")
    print(f"Orçamento: R$ {dados['orcamento']:.2f}")
    print(f"Status: {dados['status']}")
    
    areas_str = ", ".join(dados['areas'])
    print(f"Áreas de Conhecimento (Set): {{{areas_str}}}")
    
    membros = dados['membros']
    print(f"Total de Membros (List): {len(membros)}")
    if membros:
        nomes_membros = [m['nome'] for m in membros] 
        print(f"Nomes dos Membros: {', '.join(nomes_membros)}")
    
    input("Pressione Enter para continuar...")


def adicionar_membro(id_projeto):
    """Adiciona um membro à Lista de membros daquele projeto."""
    limpar_terminal()
    try:
        dados = projetos[id_projeto]
    except KeyError:
        print(f"\n[ERRO] Projeto com ID {id_projeto} não encontrado.")
        input("Pressione Enter para continuar...")
        return

    if dados['status'] == 'CONCLUÍDO':
        print(f"\n[ATENÇÃO] Projeto '{dados['titulo']}' está concluído. Não é possível adicionar novos membros.")
        input("Pressione Enter para continuar...")
        return

    print(f"\n--- Adicionar Membro ao Projeto: {dados['titulo']} ---")
    m_nome = input("Nome do Membro: ")
    m_funcao = input("Função no Projeto: ")
    
    # Verifica se o membro já está no projeto (simplesmente pelo nome)
    if any(m['nome'].lower() == m_nome.lower() for m in dados['membros']):
        print(f"\n[ATENÇÃO] O membro '{m_nome}' já faz parte deste projeto.")
        input("Pressione Enter para continuar...")
        return

    membro = {
        "nome": m_nome,
        "funcao": m_funcao
    }
    
    dados['membros'].append(membro)
    
    print(f"\n[SUCESSO] {m_nome} adicionado(a) ao projeto '{dados['titulo']}'.")
    input("Pressione Enter para continuar...")

def atualizar_status(id_projeto):
    """Atualiza o status do projeto."""
    limpar_terminal()
    try:
        dados = projetos[id_projeto]
    except KeyError:
        print(f"\n[ERRO] Projeto com ID {id_projeto} não encontrado.")
        input("Pressione Enter para continuar...")
        return

    print(f"\n--- Atualizar Status do Projeto: {dados['titulo']} ---")
    print(f"Status Atual: {dados['status']}")
    
    novos_status = ["PENDENTE", "EM ANDAMENTO", "CONCLUÍDO", "CANCELADO"]
    print("Opções de Status:")
    for i, status in enumerate(novos_status):
        print(f"{i+1}. {status}")
        
    while True:
        try:
            escolha = int(input("Escolha o novo status (1-4): "))
            if 1 <= escolha <= 4:
                novo_status = novos_status[escolha - 1]
                break
            else:
                print("[ERRO] Opção inválida.")
        except ValueError:
            print("[ERRO] Entrada inválida. Digite um número.")

    dados['status'] = novo_status
    print(f"\n[SUCESSO] Status do projeto '{dados['titulo']}' atualizado para '{novo_status}'.")
    input("Pressione Enter para continuar...")


def menu_principal():
    """Exibe o menu de opções e recebe a escolha do usuário."""
    while True:
        limpar_terminal()
        print("\n" + "="*50)
        print(f"  {INFO_SISTEMA[0]} - Gestão de Projetos de Pesquisa") 
        print("="*50)
        print("1. Iniciar Novo Projeto")
        print("2. Listar Projetos")
        print("3. Detalhar Projeto")
        print("4. Adicionar Membro à Equipe")
        print("5. Atualizar Status do Projeto")
        print("6. Sair")
        print("="*50)
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            adicionar_projeto()
        elif escolha == '2':
            listar_projetos()
        elif escolha == '3':
            try:
                id_detalhe = int(input("Digite o ID do projeto para detalhar: "))
                detalhar_projeto(id_detalhe)
            except ValueError:
                print("\n[ERRO] ID deve ser um número inteiro.")
                input("Pressione Enter para continuar...")
        elif escolha == '4':
            try:
                id_membro = int(input("Digite o ID do projeto para adicionar membro: "))
                adicionar_membro(id_membro)
            except ValueError:
                print("\n[ERRO] ID deve ser um número inteiro.")
                input("Pressione Enter para continuar...")
        elif escolha == '5':
            try:
                id_status = int(input("Digite o ID do projeto para atualizar o status: "))
                atualizar_status(id_status)
            except ValueError:
                print("\n[ERRO] ID deve ser um número inteiro.")
                input("Pressione Enter para continuar...")
        elif escolha == '6':
            limpar_terminal()
            print("Encerrando o ResearchFlow. Até mais!")
            break
        else:
            print("\n[ERRO] Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()