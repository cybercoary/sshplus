#/bin/bash
clear
echo -e "\E[38;1;33mATUALIZANDO REPOSITÓRIOS, AGUARDE..."
echo -e "\E[38;1;33m @cybercoari ☆☆☆☆☆"
echo -e "\E[38;1;33m https://cybercoari.com.br"
sleep 3
apt update; apt upgrade -y; clear
echo -e "Instalado gerenciador de arquivos compatctados..."
sleep 2
apt install zip -y; apt install unzip -y
cd /etc; rm -rf ssl stunnel; clear
echo -e "Substituindo certificados SSL..."
sleep 3
wget --no-check-certificate https://cybercoari.com.br/sshplus/Modulos/ssl.zip
unzip ssl.zip; rm ssl.zip; clear
echo -e "Atualização do certificado SSL concluída"
echo -e "Reinicie o servidor para que as mudancas "
echo -e "entrem em vigor imediatamente!!"
echo ""
cd; rm ssl.sh