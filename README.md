#install packages pip
1. apt update 
2. apt install python3-pip
3. pip --version #untuk melihat versi pip
4. pip3 install --upgrade pip
5. pip3 install paramiko #untuk menginstall paramiko
6. pip3 freeze (untuk mengecek apakah paramiko berhasil didownload)

#konfigurasi pra instalasi flask didebain server
1. su -
2. pip3 install virtualenv
3. mkdri network-automations-tools (membuat directory project untuk menyimpan file file)
4. cd network-automation-tools
5. virtualenv env (membuat lingkungan directory)
6. source env/bin/activate (untuk mengaktifkan directory)
   
#instalasi flask didebian server
1. pip3 install flask
#struktur directory network-automation-tools 
1. -project
2. app.py
   
1. -templates
2. index.html
3. output.html
4. dll...

if __name__ == '__main__':
    app.run(host="10.10.10.4", port=8000, debug=True) 
    note "sesuaikan ip host nya dan port nya"

#jalan nya flask nya 
1. python3 app.py
