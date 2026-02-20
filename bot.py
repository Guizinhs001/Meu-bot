import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Configuração de Logging ---
# Configura o sistema de logging para exibir informações no console.
# Isso é útil para depuração e para monitorar o que o bot está fazendo.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Obtém um logger para este módulo.
logger = logging.getLogger(__name__)

# --- Handlers de Comandos e Callbacks ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manipula o comando /start.
    Quando o usuário envia /start, o bot responde com uma mensagem
    e um botão de teclado embutido (inline keyboard).
    """
    logger.info(f"Comando /start recebido de {update.effective_user.full_name}")

    # Cria um botão de teclado embutido.
    # InlineKeyboardButton(texto_do_botao, dados_de_callback)
    # 'texto_do_botao' é o texto que o usuário verá no botão.
    # 'dados_de_callback' é uma string que será enviada de volta ao bot
    # quando o botão for pressionado. Usamos isso para identificar qual botão foi clicado.
    botao = InlineKeyboardButton("Clique Aqui!", callback_data="meu_botao_unico")

    # Cria um teclado embutido.
    # InlineKeyboardMarkup recebe uma lista de listas de botões.
    # Cada lista interna representa uma linha de botões.
    teclado = InlineKeyboardMarkup([[botao]])

    # Envia a mensagem com o teclado embutido.
    # 'reply_markup' é o argumento que anexa o teclado à mensagem.
    await update.message.reply_text(
        "Olá! Clique no botão abaixo:", reply_markup=teclado
    )
    logger.info("Mensagem com botão enviada.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manipula os callbacks de botões de teclado embutidos.
    Esta função é chamada quando um usuário clica em um botão com 'callback_data'.
    """
    # CallbackQuery representa uma consulta de callback de um botão embutido.
    query = update.callback_query

    # Sempre responda à consulta de callback.
    # Isso é importante para que o Telegram saiba que a consulta foi processada.
    # Caso contrário, o botão permanecerá em um estado de "carregamento" para o usuário.
    # Você pode opcionalmente enviar um pequeno aviso pop-up usando 'text' aqui.
    await query.answer()

    logger.info(f"Callback query recebida: {query.data} de {query.from_user.full_name}")

    # Verifica qual botão foi pressionado através do 'callback_data'.
    if query.data == "meu_botao_unico":
        # Edita a mensagem original para mostrar que o botão foi clicado.
        # Isso evita enviar uma nova mensagem e mantém o chat mais limpo.
        await query.edit_message_text(text=f"Botão clicado! Obrigado por interagir.")
        logger.info("Mensagem editada após clique no botão.")
    else:
        # Para lidar com qualquer outro callback_data inesperado.
        await query.edit_message_text(text="Ops! Ação desconhecida para este botão.")
        logger.warning(f"Callback data desconhecido: {query.data}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manipula erros que ocorrem durante o processamento de atualizações.
    Registra os detalhes do erro para depuração.
    """
    logger.error(f"Erro ao processar atualização: {context.error}", exc_info=context.error)
    # Opcional: Notificar o usuário ou um administrador sobre o erro.
    if update.effective_chat:
        await update.effective_chat.send_message(
            "Desculpe, ocorreu um erro inesperado. Por favor, tente novamente mais tarde."
        )


# --- Função Principal para Iniciar o Bot ---
def main() -> None:
    """
    Ponto de entrada principal do bot.
    Inicializa o bot, registra os handlers e inicia o loop de polling.
    """
    # Obtém o token do bot de uma variável de ambiente.
    # É uma boa prática de segurança NÃO embutir o token diretamente no código.
    # Antes de executar, defina a variável de ambiente BOT_TOKEN:
    # No Linux/macOS: export BOT_TOKEN="SEU_TOKEN_AQUI"
    # No Windows (cmd): set BOT_TOKEN="SEU_TOKEN_AQUI"
    # No Windows (PowerShell): $env:BOT_TOKEN="SEU_TOKEN_AQUI"
    # Certifique-se de substituir "SEU_TOKEN_AQUI" pelo token real do seu bot.
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        logger.critical(
            "Variável de ambiente 'BOT_TOKEN' não encontrada. "
            "Por favor, defina-a com o token do seu bot."
        )
        raise ValueError(
            "O token do bot não foi fornecido. Defina a variável de ambiente BOT_TOKEN."
        )

    # Constrói a aplicação do bot.
    # Usa `Application.builder().token(bot_token).build()` para criar uma instância da aplicação.
    application = Application.builder().token(bot_token).build()
    logger.info("Aplicação do bot construída.")

    # --- Registro de Handlers ---
    # Handlers são funções que o bot executa em resposta a eventos específicos.

    # 1. CommandHandler: Responde a comandos como /start, /help, etc.
    # 'start' é o nome do comando que será capturado.
    # 'start' (sem aspas) é a função assíncrona que será executada.
    application.add_handler(CommandHandler("start", start))
    logger.info("Handler para /start registrado.")

    # 2. CallbackQueryHandler: Responde a cliques em botões de teclado embutidos.
    # Nenhuma string é necessária aqui, pois ele pega qualquer CallbackQuery.
    # A lógica para diferenciar os botões está dentro da função 'button_callback'.
    application.add_handler(CallbackQueryHandler(button_callback))
    logger.info("Handler para CallbackQuery registrado.")

    # 3. ErrorHandler: Captura e loga quaisquer exceções não tratadas.
    application.add_error_handler(error_handler)
    logger.info("Handler de erro registrado.")

    # Inicia o bot.
    # 'run_polling' bloqueia a execução e verifica novas atualizações do Telegram
    # em intervalos regulares. Este é o método mais comum para bots simples.
    logger.info("Bot iniciando polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot encerrado.")


# Garante que a função main() seja chamada apenas quando o script for executado diretamente.
if __name__ == "__main__":
    main()
