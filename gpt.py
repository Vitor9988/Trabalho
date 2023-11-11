import speech_recognition as sr
import openai

openai.api_key = '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'

def obter_resposta(usuario_entrada):
    resposta = openai.Completion.create(
      engine="text-davinci-003",
      prompt=usuario_entrada,
      max_tokens=150
    )

    
    resposta_texto = resposta.choices[0].text.strip()
    return resposta_texto

def ouvir_microfone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo:")
        audio = recognizer.listen(source)
        try:
            entrada = recognizer.recognize_google(audio, language="pt-BR")
            print("Você disse:", entrada)
            return entrada
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio. Tente novamente.")
            return ""
        except sr.RequestError as e:
            print(f"Erro no reconhecimento de voz: {e}")
            return ""


def main():
    print("Bem-vindo ao Jarvis boiola! Você pode sair a qualquer momento digitando 'sair'.")
    
    while True:
        usuario_entrada = ouvir_microfone()
        
        if usuario_entrada.lower() == 'sair':
            print("Até mais!")
            break

        resposta = obter_resposta(usuario_entrada)


        print("ChatGPT:", resposta)

if __name__ == "__main__":
    main()
