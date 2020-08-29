#!/bin/bash
ENV=$1
echo "RUNNING FOR ENV: ${ENV}"
run_sam () {
    set +e
    STDERR=$(( make deploy "$@" ) 2>&1)
    ERROR_CODE=$?
    echo "CALLED FOR: ${@}"
    echo "RESPONSE CODE: ${ERROR_CODE}"
    if [[ "${ERROR_CODE}" -ne "0" ]]; then 
        echo ${STDERR} 1>&2
    fi

    if [[ "${ERROR_CODE}" -eq "2" && "${STDERR}" =~ "No changes to deploy" ]]; then 
        echo "THIS IS OK: Means no changes needed"
        set -e    
        return 0; 
    fi 
    set -e
    echo "RETURNING: ${ERROR_CODE}"
    return ${ERROR_CODE}
}

run_sam_ssm () {
    set +e
    STDERR=$(( make deploy-ssm "$@" ) 2>&1)
    ERROR_CODE=$?
    echo "CALLED FOR: ${@}"
    echo "RESPONSE CODE: ${ERROR_CODE}"
    if [[ "${ERROR_CODE}" -ne "0" ]]; then 
        echo ${STDERR} 1>&2
    fi

    if [[ "${ERROR_CODE}" -eq "2" && "${STDERR}" =~ "No changes to deploy" ]]; then 
        echo "THIS IS OK: Means no changes needed"
        set -e    
        return 0; 
    fi 
    set -e
    echo "RETURNING: ${ERROR_CODE}"
    return ${ERROR_CODE}
}


run_sam ENVIRONMENT=${ENV:-dev} SOURCE='aws-sam-kv' 
run_sam ENVIRONMENT=${ENV:-dev} SOURCE='update-table-with-yesterday'
run_sam ENVIRONMENT=${ENV:-dev} SOURCE='scrape-main-info' 
run_sam ENVIRONMENT=${ENV:-dev} SOURCE='tester' 

rm -rf templates/packaged-*