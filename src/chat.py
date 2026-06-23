from search import search_prompt

def main():
    chain = search_prompt()

    print("Chat iniciado. Digite 'sair' (ou Ctrl+C) para encerrar.\n")

    while True:
        try:
            pergunta = input("Faça sua pergunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break
        
        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break

        resposta = chain(pergunta)
        print(f"\nPERGUNTA: {pergunta}")
        print(f"RESPOSTA: {resposta}\n")
        print("-" * 40)

if __name__ == "__main__":
    main()