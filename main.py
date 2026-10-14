import argparse
import sys
from rag_exp import Vectorizer, DBManager


def main():
    parser = argparse.ArgumentParser(description="RAG Experiment CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # vectorize subcommand
    vectorize_parser = subparsers.add_parser("vectorize", help="Vectorize text and store in DB")
    vectorize_parser.add_argument("text", help="Text to vectorize and store")
    vectorize_parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2", 
                                  help="Sentence transformer model name")
    
    # query subcommand
    query_parser = subparsers.add_parser("query", help="Search for similar vectors in DB")
    query_parser.add_argument("query", help="Query text to search")
    query_parser.add_argument("--top-k", type=int, default=3, help="Number of results to return")
    query_parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2",
                              help="Sentence transformer model name")
    
    # clear subcommand
    clear_parser = subparsers.add_parser("clear", help="Clear all vectors from DB")
    
    # list subcommand
    list_parser = subparsers.add_parser("list", help="List all vectors in DB")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    vectorizer = Vectorizer(model_name=args.model)
    db_manager = DBManager()
    
    if args.command == "vectorize":
        element = db_manager.add_vector(args.text, vectorizer.text_to_vector(args.text))
        print(f"Stored vector for: '{element.text}'")
    
    elif args.command == "query":
        query_vector = vectorizer.text_to_vector(args.query)
        results = db_manager.search_top_k(query_vector, k=args.top_k)
        
        print(f"\nQuery: '{args.query}'")
        print(f"Top {len(results)} results:")
        for i, (text, similarity) in enumerate(results, 1):
            print(f"{i}. {text} (similarity: {similarity:.4f})")
    
    elif args.command == "clear":
        db_manager.clear()
        print("Database cleared")
    
    elif args.command == "list":
        elements = db_manager.get_all()
        if not elements:
            print("Database is empty")
        else:
            print(f"Database contains {len(elements)} entries:")
            for i, element in enumerate(elements, 1):
                vector_status = "stored" if element.vector is not None else "no vector"
                print(f"{i}. {element.text} ({vector_status})")


if __name__ == "__main__":
    main()
