#!/bin/sh
port=$1
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport ${port} -j ACCEPT
iptables -I INPUT -m state --state NEW -m udp -p udp --dport ${port} -j ACCEPT
ip6tables -I INPUT -m state --state NEW -m tcp -p tcp --dport ${port} -j ACCEPT
ip6tables -I INPUT -m state --state NEW -m udp -p udp --dport ${port} -j ACCEPT

iptables-save > /etc/iptables.up.rules
ip6tables-save > /etc/ip6tables.up.rules