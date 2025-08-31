from search import search_prompt

def main():
    question = input("PERGUNTA: ")
    chain = search_prompt(question)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("RESPOSTA: ", chain.invoke({"pergunta": question}))

if __name__ == "__main__":
    main()