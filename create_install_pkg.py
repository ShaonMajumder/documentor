from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException,TimeoutException,NoSuchElementException,WebDriverException,ElementNotVisibleException
import os
import time
import shutil
import platform
import subprocess
import shaonutil

package_name = 'shaonutil'

def execute_shell(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def cleaning_before_commit():
	files= package_name+""".egg-info
build
dist
.eggs
geckodriver.log
"""
	print("Cleaning files -",files)

	files = files.split('\n')

	for file in files:
		if os.path.exists(file):
			try:
				shutil.rmtree(file)
			except:
				os.remove(file)

def get_version_name():
	lines = shaonutil.file.read_file('setup.py')
	i = 0
	for line in lines:
		if '__version__' in line:
			marker = '\''
			s = line
			start = s.find(marker) + len(marker)
			end = s.find(marker, start)
			vname = s[start:end]
			break
		i+=1
	return vname
	
	

def changing_version_name(prev_vname,new_vname):
	lines = shaonutil.file.read_file('setup.py')

	strs ='\n'.join(lines)
	strs = strs.replace(prev_vname,new_vname)
	shaonutil.file.write_file('setup.py',strs)

def changing_version_name_prev(new_vname):
	lines = shaonutil.file.read_file('setup.py')

	i = 0
	for line in lines:
		if '__version__' in line:
			marker = '\''
			s = line
			start = s.find(marker) + len(marker)
			end = s.find(marker, start)
			vname = s[start:end]
			s = s.replace(vname,new_vname)
			break
		i+=1
	
	lines[i] = s
	strs = '\n'.join(lines)
	shaonutil.file.write_file('setup.py',strs)
	
def make_config():
	"""
	package_name
	initial_version
	#0.0.0.0.1
	author
	author_email
	git_project_url
	download_url
	keywords
	"""
	pass




def checks_folder():
	print("Checking the required files/folders ...")
	folders = """README.md
requirements.txt
.git
LICENSE
setup.py"""

	folders = folders.split('\n')
	for folder in folders:
		if not os.path.exists(folder):
			print("Warning :",folder,"does not exist.")


def check_modules():
	print("Checking the required modules ...")
	modules = """setuptools
wheel
twine
pipreqs"""
	modules = modules.split('\n')
	
	for module in modules:
		found = shaonutil.file.package_exists(module)
		if not found:
			print(module," package is not installed.")
			print(module," package is installing.")

			if platform.system() == 'Linux':
				command = """pip3 install """+module
			elif platform.system() == 'Windows':
				command = """pip3 install """+module

			for path in execute_shell(command):
			    print(path, end="")


def commit_push():
	commit_msg = input("Give Commit Message : ")

	if platform.system() == 'Linux':
		commands = """git add .
git commit -m \""""+commit_msg+"""\";
git push -u origin master"""
	elif platform.system() == 'Windows':
		commands = """git add .
git commit -m \""""+commit_msg+"""\";
git push -u origin master"""

	commands = commands.split("\n")

	for command in commands:
		for path in execute_shell(command):
		    print(path, end="")




def make_release(release_tag,git_url,github_user,github_pass):
	git_url = git_url + '/releases/new'
	print("Making release ...")
    
    
	if platform.system() == 'Linux':
		driver_path_firefox = 'resources/geckodriver'
	elif platform.system() == 'Windows':
		driver_path_firefox = 'resources/geckodriver.exe'


	options = Options()
	#options.headless = True
	try:
	    driver = webdriver.Firefox(executable_path=driver_path_firefox,options=options)
	except WebDriverException:
	    raise WebDriverException("invalid argument: can't kill an exited process\n Check if Firefox version and geckodriver in resources folder is not matched")
	
	driver.get('https://github.com')
	driver.find_element_by_xpath('//a[@href="/login" and contains(@data-ga-click,"text:sign-in")]').click()
	driver.find_element_by_xpath('//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]').click()
	driver.find_element_by_xpath('//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]').send_keys(github_user)
	driver.find_element_by_xpath('//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]').click()
	driver.find_element_by_xpath('//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]').send_keys(github_pass)
	driver.find_element_by_xpath('//input[@type="submit" and @name="commit" and @value="Sign in"]').click()
	driver.get(git_url)
	driver.find_element_by_xpath('//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]').click()
	driver.find_element_by_xpath('//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]').send_keys(release_tag)
	driver.find_element_by_xpath('//button[contains(@class,"js-publish-release") and @type="submit" and text()="Publish release"]').click()
	
	try:
		link_release = driver.find_element_by_xpath('//a[contains(@href,"releases/tag/0.0.0.27.1") and text()="0.0.0.27.1"]')
		driver.close()
		driver.quit()
		return True
	except:
		driver.close()
		driver.quit()
		#raise NoSuchElementException('Release was not created.')
		print('Release was not created.')
		return False

	
	


	
def upload_to_pypi(pypi_user,pypi_pass):
	
	if platform.system() == 'Linux':
		commands = """twine upload dist/* --user="""+pypi_user+""" --pass="""+pypi_pass
	elif platform.system() == 'Windows':
		commands = """twine upload dist/* --user="""+pypi_user+""" --pass="""+pypi_pass

	commands = commands.split("\n")

	for command in commands:
		for path in execute_shell(command):
		    print(path, end="")

def create_dist():
	if platform.system() == 'Linux':
		commands = """python3 setup.py sdist bdist_wheel"""
	elif platform.system() == 'Windows':
		commands = """python setup.py sdist bdist_wheel"""

	commands = commands.split("\n")

	for command in commands:
		for path in execute_shell(command):
		    print(path, end="")

def locally_install():
	if platform.system() == 'Linux':
		commands = """pip3 uninstall """+package_name+""" -y
python3 setup.py install"""
	elif platform.system() == 'Windows':
		commands = """pip3 uninstall """+package_name+""" -y
python setup.py install"""


	commands = commands.split("\n")

	for command in commands:
		for path in execute_shell(command):
		    print(path, end="")


if __name__ == '__main__':
	check_modules()
	checks_folder()

	pre_vname = get_version_name()
	print("Showing Previous Version :",pre_vname)
	new_vname = input("Give    New Version Name : ")

	changing_version_name(pre_vname,new_vname)

	cleaning_before_commit()

	commit_push()
	
	config = shaonutil.file.read_configuration_ini('private/package.config')
	git_url = config['PACKAGE']['github_project_url']
	github_user = config['PACKAGE']['github_user']
	github_pass = config['PACKAGE']['github_pass']
	release_tag = input("Give New Release tag : ")
	make_release(release_tag,git_url,github_user,github_pass)

	### git diff-index --quiet HEAD || git commit -m \""""+commit_msg+"""\";

	create_dist()

	pypi_user = config['PACKAGE']['pypi_user']
	pypi_pass = config['PACKAGE']['pypi_pass']
	# pypi_user = input("Give pypi user : ")
	# pypi_pass = input("Give pypi pass : ")
	upload_to_pypi(pypi_user,pypi_pass)

	locally_install()

	cleaning_before_commit()