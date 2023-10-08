import routeros_api
import paramiko
import time
from flask import Flask, render_template, request, redirect, session,make_response


app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Route for the home page
@app.route('/')
def home():
    return render_template('login.html')


# Route for handling the form submission
@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Handle POST request
        # Get form data
        host = request.form['host']
        username = request.form['username']
        password = request.form['password']

        # Store the connection details in session
        session['host'] = host
        session['username'] = username
        session['password'] = password

        # Establish connection to MikroTik
        connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
        api = connection.get_api()

         # Get the identity of the router
        identity = api.get_resource('/system/identity')
        router_identity = identity.get()[0]['name']


        # Define the path and retrieve the results
        list_ppp = api.get_resource('ppp/active/')
        show_ppp = list_ppp.get()

        # Close the connection
        connection.disconnect()

        return render_template('index.html', show_ppp=show_ppp, router_identity=router_identity)
    else:
        # Handle GET request to display the Active Connection page
        # Check if the session data is available
        if 'host' in session and 'username' in session and 'password' in session:
            host = session['host']
            username = session['username']
            password = session['password']

            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

                     # Get the identity of the router
            identity = api.get_resource('/system/identity')
            router_identity = identity.get()[0]['name']
            # Define the path and retrieve the results

            list_ppp = api.get_resource('ppp/active/')
            show_ppp = list_ppp.get()

            # Close the connection
            connection.disconnect()

            return render_template('index.html', show_ppp=show_ppp, router_identity=router_identity)

        # If session data is not available, redirect to login
        return redirect('/')


# Route for handling the remote action
@app.route('/remote', methods=['POST'])
def remote():
    ip_address = request.form['ip_address']

    # Redirect the user to the modem administration page
    admin_url = f"http://{ip_address}/"  # Ganti dengan URL sesuai dengan modem Anda
    return redirect(admin_url)


# Route for displaying PPPoE results
@app.route('/result/result_pppoe')
def result_pppoe():
    # Retrieve connection details from session
    host = session['host']
    username = session['username']
    password = session['password']

    # Establish connection to MikroTik
    connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
    api = connection.get_api()

    identity = api.get_resource('/system/identity')
    router_identity = identity.get()[0]['name']

    # Get PPP/Secret data
    ppp = api.get_resource('/ppp/secret')
    show_ppp = ppp.get()

    # Get profile data
    profile = api.get_resource('/ppp/profile')
    show_profile = profile.get()

    # Close the connection
    connection.disconnect()

    # Render the result_pppoe.html template with the PPP/Secret data and profile data
    return render_template('pppoe.html', show_ppp=show_ppp, show_profile=show_profile, router_identity=router_identity)


# Route for disabling PPPoE
@app.route('/result/result_pppoe/disable_pppoe', methods=['POST'])
def disable_pppoe():
    pppoe_id = request.form['pppoe_id']

    # Retrieve connection details from session
    host = session['host']
    username = session['username']
    password = session['password']

    # Establish connection to MikroTik
    connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
    api = connection.get_api()

    # Get PPP/Secret data
    ppp = api.get_resource('/ppp/secret')
    ppp.set(id=pppoe_id, disabled="true")  # Menggunakan metode set untuk menonaktifkan PPPoE

    # Close the connection
    connection.disconnect()

    return redirect('/result/result_pppoe')


# Route for Enable PPPoE
@app.route('/result/result_pppoe/enable_pppoe', methods=['POST'])
def enable_pppoe():
    pppoe_id = request.form['pppoe_id']

    # Retrieve connection details from session
    host = session['host']
    username = session['username']
    password = session['password']

    # Establish connection to MikroTik
    connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
    api = connection.get_api()

    # Get PPP/Secret data
    ppp = api.get_resource('/ppp/secret')
    ppp.set(id=pppoe_id, disabled="false")  # Menggunakan metode set untuk mengaktifkan PPPoE

    # Close the connection
    connection.disconnect()

    return redirect('/result/result_pppoe')


# Route for handling the form submission to add PPPoE secret
@app.route('/result/result_pppoe/add_secret', methods=['POST'])
def add_secret():
    name = request.form['name']
    secret_pass = request.form['secret_pass']
    service = request.form['service']
    profile = request.form['profile']

    # Retrieve connection details from session
    host = session['host']
    username = session['username']
    password = session['password']

    # Establish connection to MikroTik
    connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
    api = connection.get_api()

    # Create a new secret with the provided data
    ppp = api.get_resource('/ppp/secret')
    ppp.add(name=name, password=secret_pass, service=service, profile=profile)

    # Close the connection
    connection.disconnect()

    return redirect('/result/result_pppoe')



# Route for logging out and clearing session data
@app.route('/logout')
def logout():
    # Clear session data
    session.clear()

    # Create a response and set cache-control header to no-cache
    response = make_response(redirect('/'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # clear cache for stablitas router
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


# Routing aktivasi zte in javascript
@app.route('/script_aktivasi_zte')
def script_aktivasi_zte():
     # Fetch the router identity here
        try:
            # Retrieve connection details from session
            host = session.get('host')
            username = session.get('username')
            password = session.get('password')

            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

            # Get the router identity
            identity = api.get_resource('/system/identity')
            router_identity = identity.get()[0]['name']

            # Close the connection
            connection.disconnect()

        except Exception as e:
            router_identity = "Unknown Router"

        return render_template('script_aktivasi.html', router_identity=router_identity)

# Routing aktivasi zte in javascript
@app.route('/script_aktivasi_fh')
def script_aktivasi_fh():
     # Fetch the router identity here
        try:
            # Retrieve connection details from session
            host = session.get('host')
            username = session.get('username')
            password = session.get('password')

            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

            # Get the router identity
            identity = api.get_resource('/system/identity')
            router_identity = identity.get()[0]['name']

            # Close the connection
            connection.disconnect()

        except Exception as e:
            router_identity = "Unknown Router"

        return render_template('script_aktivasi_1.html', router_identity=router_identity)


@app.route('/cli', methods=['GET', 'POST'])
def cli():
    if request.method == 'POST':
        command = request.form['command']

        # Retrieve connection details from session
        host = session.get('host')
        username = session.get('username')
        password = session.get('password')

        try:
            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

            try:
                # Execute the command
                resource = api.get_resource(command)  # Use the user-provided command
                response = resource.get()

                # Extract the output from the response
                output = "\n".join(str(item) for item in response)

            except Exception as e:
                return render_template('cli.html', error='An error occurred while executing the command: {}'.format(str(e)))

            # Close the connection
            connection.disconnect()

            return render_template('cli.html', command=command, output=output)

        except Exception as e:
            return render_template('login.html', error='An error occurred during the connection to MikroTik: {}'.format(str(e)))

    else:
        # Fetch the router identity here
        try:
            # Retrieve connection details from session
            host = session.get('host')
            username = session.get('username')
            password = session.get('password')

            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

            # Get the router identity
            identity = api.get_resource('/system/identity')
            router_identity = identity.get()[0]['name']

            # Close the connection
            connection.disconnect()

        except Exception as e:
            router_identity = "Unknown Router"

        return render_template('cli.html', router_identity=router_identity)


@app.route('/olt')
def olt():
     # Fetch the router identity here
        try:
            # Retrieve connection details from session
            host = session.get('host')
            username = session.get('username')
            password = session.get('password')

            # Establish connection to MikroTik
            connection = routeros_api.RouterOsApiPool(host, username=username, password=password, plaintext_login=True)
            api = connection.get_api()

            # Get the router identity
            identity = api.get_resource('/system/identity')
            router_identity = identity.get()[0]['name']

            # Close the connection
            connection.disconnect()

        except Exception as e:
            router_identity = "Unknown Router"

        return render_template('olt.html', router_identity=router_identity)


@app.route('/ssh', methods=['POST'])
def ssh():
    ip_address = request.form['ip_address']
    username = request.form['username'] or "username olt" 
    password = request.form['password'] or "password olt"
    command = request.form['command']

    try:
        # Membuat objek SSHClient
        ssh = paramiko.SSHClient()
        # Menonaktifkan kebijakan SSH yang tidak aman secara default
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Membuat koneksi SSH ke OLT
        ssh.connect(ip_address, username=username, password=password)
        # Menjalankan perintah di OLT
        stdin, stdout, stderr = ssh.exec_command(command)
        # Membaca hasil keluaran perintah
        output = stdout.read().decode('utf-8')

        # Menambahkan jeda 5 detik
        time.sleep(5)

        return render_template('olt.html', output=output)

    except paramiko.AuthenticationException:
        error_message = "Autentikasi gagal. Pastikan username dan password benar."
        return render_template('olt.html', error=error_message)

    except paramiko.SSHException as ssh_exception:
        error_message = "Terjadi kesalahan SSH: " + str(ssh_exception)
        return render_template('olt.html', error=error_message)

    except paramiko.SSHException as e:
        error_message = "Terjadi kesalahan koneksi: " + str(e)
        return render_template('olt.html', error=error_message)

    finally:
        # Menutup koneksi SSH
        ssh.close()



if __name__ == '__main__':
    app.run(host="10.10.10.4", port=8000, debug=True)