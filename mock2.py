import os
import shutil
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
fake = Faker('pt_BR') # Configurado para gerar dados brasileiros (como CPF/Telefone)
URL = "https://demoqa.com/automation-practice-form"
SCREENSHOT_DIR = 'screenshots_faker'

# Limpeza da pasta de prints específica para o Faker
if os.path.exists(SCREENSHOT_DIR):
    shutil.rmtree(SCREENSHOT_DIR)
os.makedirs(SCREENSHOT_DIR)

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def executar_rpa_faker(quantidade):
    for i in range(quantidade):
        try:
            driver.get(URL)
            wait = WebDriverWait(driver, 25)

            # --- GERAÇÃO DINÂMICA COM FAKER ---
            f_name = fake.first_name()
            l_name = fake.last_name()
            email = fake.email()
            # Gera um número de 10 dígitos (padrão exigido pelo site)
            phone = fake.msisdn()[-10:] 
            # Formata a data no padrão 'dd MMM yyyy' que o DemoQA aceita
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%d %b %Y')
            address = fake.address().replace('\n', ', ')
            # ----------------------------------

            # Preenchimento
            wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys(f_name)
            driver.find_element(By.ID, "lastName").send_keys(l_name)
            driver.find_element(By.ID, "userEmail").send_keys(email)
            
            # Gênero aleatório
            gender_id = f"gender-radio-{fake.random_int(min=1, max=3)}"
            label_gender = driver.find_element(By.CSS_SELECTOR, f"label[for='{gender_id}']")
            driver.execute_script("arguments[0].click();", label_gender)

            driver.find_element(By.ID, "userNumber").send_keys(phone)

            # Data de Nascimento
            date_input = driver.find_element(By.ID, "dateOfBirthInput")
            date_input.send_keys(Keys.CONTROL + "a")
            date_input.send_keys(birth_date)
            date_input.send_keys(Keys.ENTER)

            driver.find_element(By.ID, "currentAddress").send_keys(address)
            
            # Submit
            submit_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            driver.execute_script("arguments[0].click();", submit_btn)

            # Print de Sucesso
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
            
            foto_path = os.path.join(SCREENSHOT_DIR, f"faker_{i+1}_{f_name}.png")
            driver.save_screenshot(foto_path)
            
            print(f"[{i+1}/{quantidade}] Criado: {f_name} {l_name} | Data: {birth_date}")
            time.sleep(1)

        except Exception as e:
            print(f"Erro no ciclo {i+1}: {e}")

# Executa para 5 cadastros aleatórios
try:
    print("Iniciando RPA com dados aleatórios (Faker)...")
    executar_rpa_faker(5)
finally:
    driver.quit()
    print(f"\nConcluído! Verifique a pasta: {SCREENSHOT_DIR}")