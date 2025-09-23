The first think that we need to do is create a new IDs de clientes de OAuth 2.0 in google cloud, this is the way we can conect python with google drive.

<p align="center">
  <img src="Imagenes del proyecto\google cloud.png" alt="Drive", width="80%">
</p>

Once we already conect with drive, You can use the ID of your folder or sheets but I will show you the information that I used for this example, The folder that I used to check the google sheets was.

<p align="center">
  <img src="Imagenes del proyecto\carpeta de Drive .png" alt="Drive", width="80%">
</p>

## This are the google sheets that I used it for the example

<h4>Elisa info.</h4>
<p align="center">
  <img src="Imagenes del proyecto/Archivo_Elisa.png" alt="Sheet#1", width="80%">
</p>

<h4>Aida 1st info.</h4>
<p align="center">
  <img src="Imagenes del proyecto/Archivo_aida_1ro.png" alt="Sheet#2", width="80%">
</p>

<h4>Aida 2nd info.</h4>
<p align="center">
  <img src="Imagenes del proyecto/Archivo_aida_2do.png" alt="Sheet#3", width="80%">
</p>

<h4>Cancho 3th info.</h4>
<p align="center">
  <img src="Imagenes del proyecto\Archivo_canchola_3ro.png" alt="Sheet#4", width="80%">
</p>

<h4>Josefina 3th info.</h4>
<p align="center">
  <img src="Imagenes del proyecto\Archivo_josefina_3ro.png" alt="Sheet#5", width="80%">
</p>

<h4>Ori lupita 2nd info.</h4>
<p align="center">
  <img src="Imagenes del proyecto/Archivo_ori_lupita_2do.png" alt="Sheet#6", width="80%">
</p>

<h4>Perla 2nd info.</h4>
<p align="center">
  <img src="Imagenes del proyecto\Archivo_perla_2do.png" alt="Sheet#7", width="80%">
</p>

## As you can see, just 2 google sheets have missing information, the Elisa and Aida files, the program , check averyone of the files, and if we find anymissing information in the first table we save the name of the owner of the file.

I used twilio to send the message

<h4>Twilio home screen</h4>
<p align="center">
  <img src="Imagenes del proyecto\Pantalla twilio.png" alt="Sheet#5", width="80%">
</p>

## At the end, I sent a message via whats app with the name of the teachers that needs to check the information in the file.

<h4>Whats app message</h4>
<p align="center">
  <img src="Imagenes del proyecto\Mensaje de whats app.jpg" alt="Sheet#5", width="40%">
</p>
<p> this message says "Hello Director, we already check the files y the folder ... and the next teachears Aida and Elsa haven't send the information yet, let's follow up to know what happen". but only if we are in the las 3 bussines days of the month    </p>

And the program is automatically checking the information every day in the ejecucion.py file, and all functions are in functions.py file.
