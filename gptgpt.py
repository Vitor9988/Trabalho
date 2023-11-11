import speech_recognition as sr
from gtts import gTTS
import pygame
import openai

openai.api_key = 'a sua API, professor'
#Não possuo condições de pagar a api do chatgpt, me perdoe :)

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

def reproduzir_audio(texto):
    tts = gTTS(text=texto, lang='pt-br')
    tts.save("resposta.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("resposta.mp3")
    pygame.mixer.music.play()
    pygame.event.wait()

def main():
    print("Bem-vindo ao Jarvis, se quiser sair a qualquer momento digite 'sair'.")
    
    while True:
        usuario_entrada = ouvir_microfone()
        
        if usuario_entrada.lower() == 'sair':
            print("Até mais!")
            break

        resposta = obter_resposta(usuario_entrada)
        print("ChatGPT:", resposta)

        reproduzir_audio(resposta)

if __name__ == "__main__":
    main()
