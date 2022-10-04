# SITLProxy
No projeto Ardupilot entrar na pasta ArduCopter e rodar o comando para criar o Drone
ardupilot/ArduCopter$ ../Tools/autotest/sim_vehicle.py -v ArduCopter -f coaxcopter -L UFF
A localização foi configurada no arquivo locations.txt. O proxy está utilizando a mesma localização.
Caso queira usar outra localização será preciso colocar também no param1 e param2 do proxy.

Comando para rodar o Proxy:
python proxySTIL.py -22.9063841 -43.1328481 0 5 teste5 teste6 teste7
param1: latitude
param2: longitude
param3: altura
param4: altura relativa
param5: não implementado
param6: não implementado
param7: não implementado

O proxy ficará esperando a conexão do MAVProxy .
Entrar na pasta /mavproxy/MAVProxy-master/MAVProxy do projeto MAVProxy e rodar o comando:
~/mavproxy/MAVProxy-master/MAVProxy$ python mavproxy.py --master=tcp:127.0.0.1:5000  --map --console

O MAVProxy vai conectar no proxy e o proxy conectará no drone fazendo a ponte de comunicação.
