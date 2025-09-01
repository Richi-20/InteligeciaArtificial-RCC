import random
import time

def lanzar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    suma = dado1 + dado2
    return dado1, dado2, suma
print("Richard Chavez Cano")
print("🎲 Bienvenido al juego de Mayor o Menor 🎲")
print("Reglas:")
print(" - Si sale entre 2 y 6 → Menor")
print(" - Si sale 7 → La casa gana 😈")
print(" - Si sale entre 8 y 12 → Mayor\n")

# Elección del jugador
while True:
    eleccion = input("¿A qué deseas apostar? (mayor/menor): ").strip().lower()
    if eleccion in ["mayor", "menor"]:
        break
    print("❌ Opción inválida. Solo puedes escribir 'mayor' o 'menor'.")

# Apuesta
while True:
    try:
        apuesta = int(input("Ingresa tu apuesta (solo números enteros): "))
        if apuesta > 0:
            break
        else:
            print("❌ La apuesta debe ser mayor a 0.")
    except ValueError:
        print("❌ Ingresa un número válido.")

print("\n🎲 Lanzando los dados... 🎲\n")
time.sleep(1)

d1, d2, suma = lanzar_dados()
print(f"Los dados cayeron: 🎲 {d1} y 🎲 {d2} → Total: {suma}")

# Evaluar resultado
if suma == 7:
    print("\n💀 ¡Salió 7! La casa gana, pierdes tu apuesta.")
    ganancia = -apuesta
elif suma <= 6 and eleccion == "menor":
    print("\n🎉 ¡FELICIDADES! Apostaste a MENOR y GANASTE 🎉")
    ganancia = apuesta * 2
elif suma >= 8 and eleccion == "mayor":
    print("\n🎉 ¡FELICIDADES! Apostaste a MAYOR y GANASTE 🎉")
    ganancia = apuesta * 2
else:
    print("\n💔 Mala suerte... Perdiste tu apuesta 💔")
    ganancia = -apuesta

print(f"\n💰 Resultado final: {'Ganaste' if ganancia>0 else 'Perdiste'} {abs(ganancia)} monedas 💰")
