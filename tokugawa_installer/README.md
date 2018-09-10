<html>
<body style="font-family: Consolas, monospace; font-size:14pt;">
<b>Tokugawa Masternode installer instructions</b>
<br/> ────────────────────────────────────────────────────
<br/>
<br/> A beautiful python installer that allows you to install your tokugawa masternodes withing minutes.
<br/>
<br/> <b>0. Requirements</b>
<br/>
<br/> In order to run this program the below python3 libraries need to be installed:
<br/> &nbsp; &nbsp; $sudo apt-get install python3-pip python3-yaml
<br/> 
<br/> In addition the following files/programms are needed:
<br/> &nbsp; &nbsp; - A precompiled binary containing the latest version of the Tokugawa daemon.
<br/> &nbsp; &nbsp; - [Optional] A bootstrap file to accelerate the initial masternode synchronisation.
<br/> &nbsp; &nbsp; - [Optional] ufw if present the firewall will be automatically configured to enable SSH/Tokugawa ports. ($apt install ufw).
<br/>
<br/> <b>1. Copying the necessary files</b>
<br/>
<br/> &nbsp; &nbsp; $mkdir -p /tmp/tokugawa_installer/
<br/> &nbsp; &nbsp; $cd /tmp/tokugawa_installer/
<br/> &nbsp; &nbsp; $wget https://raw.githubusercontent.com/Lyndros/crypto_tools/master/tokugawa_installer/tokugawa_installer.py
<br/>
<br/> -- This is a configuration example, please modify as needed before running the installer--
<br/> &nbsp; &nbsp; $wget https://raw.githubusercontent.com/Lyndros/crypto_tools/master/tokugawa_installer/masternodes.yml
<br/>
<br/> &nbsp; &nbsp; In addition get your tokugawad binary from your favourite source or compile it.
<br/> &nbsp; &nbsp; A bootstrap.dat file is optional but very recommended if you want to have your MNs running asap.
<br/>
<br/> <b>2. Setting your configuration file</b>
<br/> 
<br/> Modify the configuration file to match your needs: mainly IP, port and masternode privkey settings...
<br/> If you run multiple masternodes in the same VPS, you can share the IP, take into account that ports must be different.
<br/>
<br/> <b>3. Running the installer</b>
<br/> &nbsp; &nbsp; $./tokugawa_installer.py <tokugawad_file> <dest_folder> <mn_configuration.yml> [ --bootstrap <bootstrap_file.dat> ]
<br/>
<br/> &nbsp; &nbsp; Execution examples:
<br/> &nbsp; &nbsp; $./tokugawa_installer.py /tmp/tokugawad /opt/usr/toku masternodes.yml --bootstrap /tmp/bootstrap.dat
<br/> &nbsp; &nbsp; $./tokugawa_installer.py /tmp/tokugawad /opt/usr/tokugawa masternodes.yml
<br/>
<br/> <b>4. Enabling tokugawa services automatically at boot</b>
<br/> &nbsp; &nbsp; $systemctl enable tokugawa
<br/> 
<br/> If during the installation ufw firewall was detected the following steps must be done:
<br/> &nbsp; &nbsp; $ufw stop; 
<br/> &nbsp; &nbsp; $ufw allow tokugawa; $ufw reload; $ufw enable; 
<br/> &nbsp; &nbsp; $systemctl enable ufw;
<br/>
<br/> <b>5. Donations</b>
<br/> If you want to motivate me and support this repository I accept donations even 1 TOK is always welcome :-)!
<br/> &nbsp; &nbsp;> <b>ethereum address:</b> <i>0x44F102616C8e19fF3FED10c0b05B3d23595211ce</i>
<br/> &nbsp; &nbsp;> <b>tokugawa address:</b> <i>TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA</i>
<br/>
<br/> For any questions feel free to contact me at <i>lyndros@hotmail.com</i>
</body>
</html>