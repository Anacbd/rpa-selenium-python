import pandas as pd
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
FILE_PATH = 'MOCK_DATA.csv'
URL = "https://demoqa.com/automation-practice-form"
SCREENSHOT_DIR = 'screenshots'

# 1. LIMPEZA: Apaga prints antigos para a pasta ficar limpa para impressão
if os.path.exists(SCREENSHOT_DIR):
    shutil.rmtree(SCREENSHOT_DIR)
os.makedirs(SCREENSHOT_DIR)

# 2. TRATAMENTO DE DADOS: Formatação da Data (Ex: 31/08/1985 -> 31 Aug 1985)
df = pd.read_csv(FILE_PATH)
# Convertemos para data e depois para o texto que o site aceita (3 letras do mês)
df['birth'] = pd.to_datetime(df['birth'], dayfirst=True).dt.strftime('%d %b %Y')
df = df.head(5) # Apenas os 5 primeiros itens como solicitado

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def preencher_formulario(row, index):
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 25) # Tolerância alta para rede lenta

        # Nome, Sobrenome e Email
        wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys(row['first_name'])
        driver.find_element(By.ID, "lastName").send_keys(row['last_name'])
        driver.find_element(By.ID, "userEmail").send_keys(row['email'])
        
        # Gênero (Clique via JavaScript para não falhar)
        gender = str(row['gender']).capitalize()
        gender_id = "gender-radio-1" if gender == 'Male' else "gender-radio-2" if gender == 'Female' else "gender-radio-3"
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, f"label[for='{gender_id}']"))

        # Telemóvel
        driver.find_element(By.ID, "userNumber").send_keys(str(row['mobile'])[:10])

        # DATA DE NASCIMENTO (Com a nova formatação dd MMM yyyy)
        date_input = driver.find_element(By.ID, "dateOfBirthInput")
        date_input.send_keys(Keys.CONTROL + "a")
        date_input.send_keys(row['birth'])
        date_input.send_keys(Keys.ENTER)

        # ENDEREÇO (Lendo a coluna 'adress' do seu CSV)
        driver.find_element(By.ID, "currentAddress").send_keys(row['adress'])
        
        # SUBMIT (Com scroll e clique via JS para evitar anúncios)
        submit_btn = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        driver.execute_script("arguments[0].click();", submit_btn)

        # ESPERA MODAL DE SUCESSO E TIRA PRINT
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
        
        foto_nome = f"sucesso_{index+1}_{row['first_name']}.png"
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, foto_nome))
        
        print(f"[{index+1}/5] OK: {row['first_name']} | Data: {row['birth']} | Endereço: {row['adress']}")
        time.sleep(1)

    except Exception as e:
        print(f"Erro no registro {index+1}: {e}")

# LOOP DE EXECUÇÃO
try:
    print("Iniciando RPA... Preparando evidências para impressão.")
    for index, row in df.iterrows():
        preencher_formulario(row, index)
finally:
    driver.quit()
    print(f"\nConcluído! As fotos estão na pasta: {os.path.abspath(SCREENSHOT_DIR)}")