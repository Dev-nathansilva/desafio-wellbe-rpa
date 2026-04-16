from movie_search import search_avengers_and_save
from invoice_extraction import extract_and_zip_invoices


def main():
    print("=== ETAPA 1: MOVIE SEARCH ===")
    search_avengers_and_save()

    print("\n=== ETAPA 2: INVOICE EXTRACTION ===")
    extract_and_zip_invoices()

    print("\nDesafio finalizado com sucesso.")


if __name__ == "__main__":
    main()