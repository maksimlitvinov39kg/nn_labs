import json
import streamlit as st
from models.rugpt3large import RUGPT3Large

def load_config(config_path):
    """Загрузка конфигурации из JSON-файла."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Конфигурационный файл не найден: {config_path}")
    except json.JSONDecodeError:
        st.error("Ошибка при чтении конфигурационного файла.")
    return None

@st.cache_resource
def init_model(config_path="config.json"):
    """Инициализация модели с кешированием."""
    config = load_config(config_path)
    if config is None:
        return None, None
    
    try:
        generator = RUGPT3Large(
            model_name_or_path=config["model_name_or_path"],
            device=config["device"]
        )
        return generator, config
    except Exception as e:
        st.error(f"Ошибка при загрузке модели: {e}")
        return None, None

def initialize_session_state():
    """Инициализация состояния сессии."""
    if 'model_initialized' not in st.session_state:
        st.session_state.model_initialized = False
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'config' not in st.session_state:
        st.session_state.config = None

def main():
    st.write("# Генерация текста с помощью ruGPT-3")
    
    initialize_session_state()
    
    # Инициализация модели только один раз
    if not st.session_state.model_initialized:
        generator, config = init_model(config_path='configs/rugpt3large.json')
        if generator and config:
            st.session_state.generator = generator
            st.session_state.config = config
            st.session_state.model_initialized = True
    
    if not st.session_state.model_initialized:
        st.error("Не удалось инициализировать модель или конфигурацию.")
        return

    # Получаем параметры генерации из конфигурации
    gen_params = st.session_state.config["generation_params"]
    
    # Интерфейс пользователя
    with st.form("generation_form"):
        prompt = st.text_area("Введите текст для продолжения", 
                            "")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_length = st.slider("Максимальная длина", 20, 500, 
                                 gen_params["max_length"])
            min_length = st.slider("Минимальная длина", 10, max_length, 
                                 gen_params["min_length"])
            temperature = st.slider("Температура", 0.1, 2.0, 
                                 gen_params["temperature"], 0.1)
            top_k = st.slider("Top-K", 1, 100, gen_params["top_k"])
            
        with col2:
            top_p = st.slider("Top-P", 0.0, 1.0, gen_params["top_p"], 0.1)
            repetition_penalty = st.slider("Штраф за повторения", 1.0, 2.0, 
                                        gen_params["repetition_penalty"], 0.1)
            num_return_sequences = st.slider("Количество вариантов", 1, 5, 
                                          gen_params["num_return_sequences"])
            do_sample = st.checkbox("Использовать сэмплинг", 
                                  gen_params["do_sample"])


        # Опциональные поля для префикса и суффикса
        with st.expander("Дополнительные параметры"):
            use_prefix = st.checkbox("Использовать префикс")
            prefix = st.text_input("Префикс", "") if use_prefix else ""
            
            use_suffix = st.checkbox("Использовать суффикс")
            suffix = st.text_input("Суффикс", "") if use_suffix else ""

        # Кнопка генерации в форме
        generate_button = st.form_submit_button("Сгенерировать текст")

    # Обработка генерации текста
    if generate_button:
        if not prompt.strip():
            st.error("Пожалуйста, введите текст для генерации.")
        else:
            with st.spinner('Генерация текста...'):
                try:
                    # Формируем полный промпт
                    full_prompt = f"{prefix}{prompt}{suffix}"
                    
                    # Параметры генерации
                    generation_params = {
                        "max_length": max_length,
                        "min_length": min_length,
                        "num_return_sequences": num_return_sequences,
                        "do_sample": do_sample,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "repetition_penalty": repetition_penalty,
                    }

                    # Генерация текста
                    generated_texts = st.session_state.generator.generate_text(
                        prompt=full_prompt,
                        **generation_params
                    )
                    
                    # Вывод результатов
                    st.success("Генерация завершена!")
                    for i, text in enumerate(generated_texts, 1):
                        with st.expander(f"Вариант {i}"):
                            st.write(text)
                            # Добавляем кнопку копирования
                            if st.button(f"Копировать вариант {i}", key=f"copy_{i}"):
                                st.write("Текст скопирован в буфер обмена!")
                                st.session_state[f'clipboard_{i}'] = text

                except Exception as e:
                    st.error(f"Ошибка при генерации текста: {str(e)}")

    # Добавляем информацию о статусе модели
    st.sidebar.info("Статус модели: Активна" if st.session_state.model_initialized 
                   else "Статус модели: Не инициализирована")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Генератор текста ruGPT-3",
        page_icon="📝",
        layout="wide"
    )
    main()