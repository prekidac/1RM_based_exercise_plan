#! /bin/bash

mojaT=77
tr_now=3 # zadnji trening
ci_now=0 # zadnji ciklus
procenti=( 105 100 97 94 92 89 86 83 81 78 75 73 71 70 )
trening=( Bench Zgib Deadlift Press Squat )
ciklus=( neural metabolic )
neural='12 9 6 3'
metabolic='12 10'

Bench=74.09 # 1RM
Zgib=23.89 #
Press=60.69 # 
Squat=83.43 #
Deadlift=112.66 # 
Crunch=6.08 # 

#: USAGE: is_num argument
is_num() {
    case "${1:-empty}" in
        *[!0-9.]* ) 
            printf "  \e[31mError: Not a number\e[m\n" >&2 
            return 1 ;;
    esac
}

#: USAGE: update var_name
update() {
    sed -i "s/${1:?Nema var_name}=.* #/$1=${!1} #/" "${0}"
}

#: USAGE: tezina_update RM
tezina_update() {
    while true; do
        read -p "  Puta podigao: " 
        if is_num "${REPLY}"; then
            if [[ ${trening[$tr_now]} == Zgib ]]; then
                eval "${trening[$tr_now]}"="$(echo "scale=2; (${!trening[$tr_now]}+$mojaT)*${procenti[$1]}/${procenti[$REPLY]}-$mojaT" | bc -l)"
            else
                eval "${trening[$tr_now]}"="$(echo "scale=2; ${!trening[$tr_now]}*${procenti[$1]}/${procenti[$REPLY]}" | bc -l)"
            fi
            break
        fi
    done
    update "${trening[$tr_now]}" 
}

#: USAGE: tezine RM  
tezine() {
    local i n tezina 
    _RM=( $1 )
    _TE=()
    
    if [[ "${trening[$tr_now]}" == 'Zgib' ]]; then
        tezina=$(echo "${!trening[$tr_now]}+${mojaT}" | bc -l)
    else
        tezina=${!trening[$tr_now]}
    fi

    for i in ${_RM[@]}; do
        _TE+=( $(echo "scale=0; ($tezina*${procenti[$i]}/250)*2.5" | bc -l) )
    done

    if [[ "${trening[$tr_now]}" == 'Zgib' ]]; then
        n=0
        for i in ${_TE[@]}; do
            if [[ $(echo "scale=0; ($i-$mojaT)/2.5*2.5<0" | bc -l) -eq 1 ]]; then
                eval _TE[$n]=0
            else
                eval _TE[$n]=$(echo "scale=0; ($i-$mojaT)/2.5*2.5" | bc -l)
            fi
            n=$(($n+1))
        done
    fi
}

#: USAGE: ispisi_trening RM  
ispisi_trening() {
    local n
    tezine "${1}"
    if [[ ${ciklus[$ci_now]} == metabolic ]]; then
        n=$((${#_TE[@]}-1))
        for i in ${_TE[@]:0:$n}; do
            printf "\t\t%s\tx %s\n" $i $((${_RM[-1]}-3))
        done
        printf "\n  \e[01;32m%-10s\e[m\t%s\tx %s\n\n" ${trening[$tr_now]}: \
            ${_TE[-1]} $((${_RM[-1]}-3))
        read -n1
    else 
        n=$((${#_TE[@]}-1))
        for i in ${_TE[@]:0:$n}; do
            printf "\t\t%s\tx %s\n" $i ${_RM[-1]} 
        done
        printf "\n  \e[01;31m%-10s\e[m\t%s\tmax\n\n" ${trening[$tr_now]}: \
            ${_TE[-1]} 
        tezina_update ${_RM[-1]}
    fi
}

odredi_trening() {
    tr_now=$(($tr_now+1))
    if [[ $tr_now -gt $((${#trening[@]}-1)) ]]; then
        tr_now=0
        ci_now=$(($ci_now+1))
        if [[ $ci_now -gt $((${#ciklus[$ci_now]}-1)) ]]; then
            ci_now=0
        fi
    fi
}

ciklus() {
    odredi_trening
    ispisi_trening "${!ciklus[$ci_now]}" 
}

clear -x
ciklus

update ci_now 
update tr_now
