import telebot

API_TOKEN = '25443586527:AAECM5wVAts2fAIJhU_NDReWiMLL4MwhUKU'
bot = telebot.TeleBot(API_TOKEN)

def countingSortForRadix(inputArray, placeValue):
    countArray = [0] * 10
    inputSize = len(inputArray)

    for i in range(inputSize):
        placeElement = (inputArray[i] // placeValue) % 10
        countArray[placeElement] += 1

    for i in range(1, 10):
        countArray[i] += countArray[i - 1]

    outputArray = [0] * inputSize
    i = inputSize - 1

    while i >= 0:
        currentEl = inputArray[i]
        placeElement = (currentEl // placeValue) % 10
        countArray[placeElement] -= 1
        newPosition = countArray[placeElement]
        outputArray[newPosition] = currentEl
        i -= 1

    return outputArray

def radixSort(inputArray):
    maxEl = max(inputArray)
    D = 0

    while maxEl > 0:
        maxEl //= 10
        D += 1

    placeVal = 1
    outputArray = inputArray

    while D > 0:
        outputArray = countingSortForRadix(outputArray, placeVal)
        placeVal *= 10
        D -= 1

    return outputArray

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.mime_type == 'text/plain':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file locally
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Read numbers from the file
        with open(message.document.file_name, 'r') as f:
            try:

                content = f.read()

                input_array = []
                for item in content.split(','):
                    item = item.strip()
                    if item:
                        try:
                            input_array.append(float(item))
                        except ValueError:
                            continue

                if not input_array:
                    raise ValueError("No valid numbers found.")

                sorted_array = radixSort(input_array)  # Sort the numbers
                bot.reply_to(message, f"Отсортированный массив из файла: {sorted_array}")
            except ValueError as ve:
                bot.reply_to(message, str(ve))
            except Exception as e:
                bot.reply_to(message, f"Произошла ошибка при обработке файла: {str(e)}")
    else:
        bot.reply_to(message, "Пожалуйста, загрузите текстовый файл (.txt).")

@bot.message_handler(commands=['numbers'])
def handle_numbers_command(message):
    try:
        input_array = []
        for item in message.text.split()[1:]:
            item = item.strip()
            if item:
                try:
                    input_array.append(float(item))
                except ValueError:
                    continue

        if not input_array:
            raise ValueError("No valid numbers provided.")

        sorted_array = radixSort(input_array)
        bot.reply_to(message, f"Отсортированный массив: {sorted_array}")
    except ValueError as ve:
        bot.reply_to(message, str(ve))
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.reply_to(message, "Привет! Используйте команду /numbers, чтобы отсортировать числа. Например: /numbers 5, -3.5, 8, 6\n\nВы также можете загрузить текстовый файл с числами.")

bot.polling()