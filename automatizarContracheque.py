from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import Select



# Set up Chrome options
chrome_options = webdriver.ChromeOptions()

# Set the directory where files will be downloaded
download_directory = "/contra"

# Configure Chrome to automatically download PDF files
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome(ChromeDriverManager().install())


try:
    # Navega para a URL
    driver.get("https://sapiranga.atende.net/autoatendimento/servicos/emissao-do-recibo-de-pagamento/detalhar/1?")
    
    # Espera até que os elementos de input e o botão estejam presentes no DOM
    wait = WebDriverWait(driver,100)

    #element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Press the 'Esc' key
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    wait = WebDriverWait(driver, 100)

    input_login = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    input_senha = wait.until(EC.presence_of_element_located((By.NAME, "senha")))
    btn_login = wait.until(EC.presence_of_element_located((By.NAME, "btn_login")))
    
    # Insere o login e a senha
    input_login.send_keys("insira seu login")
    input_senha.send_keys("insira sua senha")
    
    # Clica no botão de login
    btn_login.click()

finally:
    time.sleep(5)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    wait = WebDriverWait(driver, 100)

    
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'aceitar_termos_cookie_privacidade')))
    
    # Click the button
    button.click()

    select_element = wait.until(EC.presence_of_element_located((By.NAME, "PeriodoFolha.odoMesAno")))

    # Create a Select instance
    select = Select(select_element)

    # Iterate through the dropdown options
    for option in select.options:
        # Select the option
        select.select_by_value(option.get_attribute("value"))
        
        # Click the button
        button = driver.find_element(By.NAME, "confirmar")
        button.click()

        time.sleep(2)

        download_script = """
        var blobUrl = document.querySelector('.pdfobject').src;
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'blob';
        xhr.onload = function() {
            var a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhr.response);
            a.download = 'downloaded_file.pdf';
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
        xhr.open('GET', blobUrl);
        xhr.send();
        """

        driver.execute_script(download_script)

        time.sleep(1)

        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'fechar_impressao_relatorio_')]")))

        # Click the close button
        close_button.click()

        # Wait for 1 second
        time.sleep(1)

    driver.quit()
