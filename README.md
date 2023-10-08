#install packages pip
1. apt update 
2. apt install python3-pip
3. pip --version #untuk melihat versi pip
4. pip3 install --upgrade pip
5. pip3 install paramiko #untuk menginstall paramiko
6. pip3 freeze (untuk mengecek apakah paramiko berhasil didownload)

#konfigurasi pra instalasi flask didebain server
su -
pip3 install virtualenv
mkdri network-automations-tools (membuat directory project untuk menyimpan file file)
cd network-automation-tools
virtualenv env (membuat lingkungan directory)
source env/bin/activate (untuk mengaktifkan directory)
#instalasi flask didebian server
pip3 install flask
	#struktur directory network-automation-tools
		-project
			app.py
		-templates
			index.html
			output.html
      dll...

if __name__ == '__main__':
    app.run(host="10.10.10.4", port=8000, debug=True)

    note : sesuaikan ip host dan port nya


jalan nya flask nya 
python3 app.py
