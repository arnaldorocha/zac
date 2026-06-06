"""
Zac Personal Assistant - Main Entry Point
"""
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/zac.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def setup_directories():
    """Create necessary directories."""
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    logger.info("Directories setup complete")


def main():
    """Main entry point."""
    setup_directories()
    
    from core.assistant import ZacAssistant
    
    try:
        logger.info("=" * 50)
        logger.info("Zac Personal Assistant Starting")
        logger.info("=" * 50)
        
        # Initialize assistant
        assistant = ZacAssistant(db_path="data/zac.db")
        
        # Greet user
        assistant.tts.speak("Olá! Eu sou Zac. Como posso ajudá-lo mestre Arnaldo?")
        
        logger.info("Assistant ready for commands")
        logger.info("Type 'quit' to exit, 'help' for commands, or speak a command")
        
        # Main loop
        while True:
            try:
                user_input = input("\nZac> ").strip().lower()
                
                if user_input == "quit":
                    logger.info("Exiting...")
                    assistant.tts.speak("Até logo!")
                    break
                
                elif user_input == "help":
                    print_help()
                
                elif user_input == "listen":
                    assistant.listen_and_execute()
                
                elif user_input == "test":
                    run_tests()
                
                elif user_input:
                    result = assistant.process_command(user_input)
                    if result:
                        print(f"\nZac: {result}")
                
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                assistant.tts.speak("Até logo!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"Erro: {e}")
        
        # Shutdown
        assistant.shutdown()
        logger.info("Zac Assistant shutdown complete")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Erro fatal: {e}")
        sys.exit(1)


def print_help():
    """Print available commands."""
    help_text = """
    ╔════════════════════════════════════════════════════════════════╗
    ║              Zac - Comandos Disponíveis                       ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║ TAREFAS:                                                       ║
    ║   "adicionar tarefa [descrição]"                              ║
    ║   "quais são minhas tarefas"                                  ║
    ║   "concluir tarefa [nome]"                                    ║
    ║                                                                ║
    ║ AGENDA:                                                        ║
    ║   "adicionar compromisso [descrição] [hora]"                  ║
    ║   "qual é minha agenda"                                       ║
    ║                                                                ║
    ║ NAVEGADOR:                                                     ║
    ║   "abrir chrome"                                              ║
    ║   "navegar para [site]"                                       ║
    ║                                                                ║
    ║ SHEETS:                                                        ║
    ║   "registrar gasto de [valor] com [categoria]"                ║
    ║   "registrar estudo de [disciplina] por [horas]"              ║
    ║                                                                ║
    ║ MEMÓRIA:                                                       ║
    ║   "lembrar que [informação]"                                  ║
    ║                                                                ║
    ║ OUTROS:                                                        ║
    ║   "listen"  - Ouvir comando de voz                            ║
    ║   "help"    - Mostrar esta mensagem                           ║
    ║   "quit"    - Sair                                            ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(help_text)


def run_tests():
    """Run basic tests."""
    print("\n" + "=" * 50)
    print("Executando testes...")
    print("=" * 50 + "\n")
    
    from tests.test_basic import run_all_tests
    run_all_tests()


if __name__ == "__main__":
    main()
