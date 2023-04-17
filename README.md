bachelor-thesis
=========================================
This bachelor thesis related project is using the Mesa Python Framework. Mesa allows users to quickly create agent-based models using built-in core components (such as spatial grids and agent schedulers) or customized implementations; in this case information dissimenation in crowded enviroments; the tool offers a variety of built-in configuraitions to visualize different szenarios and analyze their results using Python's data analysis tools. 

.. image:: https://raw.githubusercontent.com/projectmesa/mesa/main/docs/images/Mesa_Screenshot.png
   :width: 100%
   :scale: 100%
   :alt: A screenshot of the Schelling Model in Mesa

*Above: A Mesa implementation of the Schelling segregation model,
being visualized in a browser window and analyzed in a Jupyter
notebook.*

Features
------------

* Modular components
* Browser-based visualization
* Built-in tools for analysis
* Example model library

Local Setup (venv)
------------

Getting started quickly:
Clone the repository:

    $ git clone https://github.com/DonSimerino/bachelor-thesis.git
    
Create a python venv with cltr + shift + P -> "Python: Create Enviroment.":

Click on the script to activate the venv:

    .venv\Scripts\Activate.ps1
    
 Install Mesa:
 
    $ pip install mesa


Now you can start the server by running the ./information/run.py:

    $ py .\simulations\information\run.py


Docker Setup
------------------------

Expected that Docker is already installed and setup and your system, this should build the image and run the server.

    $ docker build . -t mymesa_image
    
If successfully built, you can start the container:

    $ docker run -v ${pwd}/simulations:/bachelor-thesis/simulations --name mymesa_instance --rm -p 8521:8521 -it mymesa_image


docker run -v $(pwd)/examples:/opt/mesa/examples --name mymesa_instance --rm -p 8521:8521 -it mymesa_image

## The MIT License (MIT)
Copyright © 2021

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
