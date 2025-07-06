#!/usr/bin/env bash

## Este script genera el archivo .env

################ Creo variables de trabajo ################

WORKSCRIPT="$(pwd)"

################ Comprueba requisitos ################

## En caso de ser root se aborta.
if [[ $(whoami) = 'root' ]]; then
    echo 'No puedes ejecutar este script como root'
    exit 1
fi

## En caso de no encontrar archivos esenciales para la ejcución se aborta.
if [[ ! -d "${WORKSCRIPT}/deploy" ]] ||
   [[ ! -f "${WORKSCRIPT}/deploy/functions.sh" ]]; then
    echo 'Este script solo puede ser ejecutado desde la raíz del proyecto.'
    exit 1
fi

################ Incluyo archivos de funciones ################

source "${WORKSCRIPT}/deploy/functions.sh"

################ Comienza el flujo de generar .env ################

## Creo el archivo .env a partir del archivo con parámetros predefinidos.

#cp "${WORKSCRIPT}/.env.example" "${WORKSCRIPT}/.env"
#chmod ug+rw "${WORKSCRIPT}/.env"

## General

#replace_or_add_var_in_file "${WORKSCRIPT}/.env" 'varname???' "${varname???}"

echo ""
#echo "Resultado del .env final:"
#cat "${WORKSCRIPT}/.env"

## Enlazo almacenamiento con los perfiles
link_data_storage "${WORKSCRIPT}"

exit 0