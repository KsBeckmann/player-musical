from menu import MenuReprodutor

if __name__ == "__main__":
    try:
        MenuReprodutor().menu_principal()
    except Exception as e:
        print(f"Erro fatal: {str(e)}")