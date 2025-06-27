from menu import MenuReprodutor

def main():
    """
    função principal que inicia a aplicação.
    """
    try:
        MenuReprodutor().menu_principal()
    except Exception as e:
        # captura exceções não tratadas para um encerramento mais seguro
        print(f"Ocorreu um erro fatal e inesperado: {str(e)}")
        # registrar o erro em um arquivo de log de falhas
        with open("crash_log.txt", "a") as f:
            import traceback
            from datetime import datetime
            f.write(f"--- {datetime.now()} ---\n")
            traceback.print_exc(file=f)
            f.write("\n")

if __name__ == "__main__":
    main()