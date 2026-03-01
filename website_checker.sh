#!/bin/bash
# ============================================
# WEBSITE CHECKER TOOL - BASH VERSION
# ============================================
# Developer: Md. Mainul Islam
# Owner: MAINUL - X
# GitHub: M41NUL
# WhatsApp: +8801308850528
# ============================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

while true; do
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                   WEBSITE CHECKER TOOL                   ║"
    echo "║                       by MAINUL - X                      ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${YELLOW}Developer: Md. Mainul Islam${NC}"
    echo -e "${YELLOW}Contact: +8801308850528${NC}"
    echo -e "${YELLOW}GitHub: M41NUL${NC}"
    echo ""
    
    echo -e "${BLUE}${BOLD}════════════════════════════════════════════${NC}"
    echo -e "${GREEN}1.${NC} Check Single Website"
    echo -e "${GREEN}2.${NC} Check Multiple Websites"
    echo -e "${GREEN}3.${NC} Website Response Time"
    echo -e "${GREEN}4.${NC} DNS Information"
    echo -e "${GREEN}5.${NC} Port Scan"
    echo -e "${GREEN}6.${NC} HTTP Headers"
    echo -e "${RED}0.${NC} Exit"
    echo -e "${BLUE}${BOLD}════════════════════════════════════════════${NC}"
    
    read -p $'\e[32mEnter option: \e[0m' option
    
    case $option in
        1)
            echo ""
            read -p $'\e[33mEnter website (e.g., google.com): \e[0m' site
            
            echo -e "${YELLOW}Checking $site...${NC}"
            
            if ping -c 2 -W 3 $site &> /dev/null; then
                ip=$(ping -c 1 $site | head -1 | grep -oP '\(\K[^)]+')
                time=$(ping -c 1 $site | tail -2 | head -1 | grep -oP 'time=\K[^ ]+')
                
                echo -e "${GREEN}✓ STATUS: UP${NC}"
                echo -e "${CYAN}IP: $ip${NC}"
                echo -e "${CYAN}Response Time: $time ms${NC}"
            else
                echo -e "${RED}✗ STATUS: DOWN${NC}"
            fi
            ;;
            
        2)
            echo ""
            echo -e "${YELLOW}Enter websites (space separated):${NC}"
            read -a sites
            
            echo ""
            echo -e "${BLUE}════════════════════════════════════════════${NC}"
            
            for site in "${sites[@]}"; do
                echo -n "$site ... "
                if ping -c 1 -W 2 $site &> /dev/null; then
                    echo -e "${GREEN}UP${NC}"
                else
                    echo -e "${RED}DOWN${NC}"
                fi
            done
            ;;
            
        3)
            echo ""
            read -p $'\e[33mEnter website: \e[0m' site
            
            echo -e "${YELLOW}Measuring response time...${NC}"
            
            for i in {1..3}; do
                time=$(ping -c 1 $site | tail -1 | grep -oP 'time=\K[^ ]+' 2>/dev/null)
                if [ ! -z "$time" ]; then
                    echo -e "  Request $i: ${CYAN}${time}ms${NC}"
                else
                    echo -e "  Request $i: ${RED}failed${NC}"
                fi
                sleep 0.5
            done
            ;;
            
        4)
            echo ""
            read -p $'\e[33mEnter website: \e[0m' site
            
            echo -e "${YELLOW}Getting DNS info...${NC}"
            
            echo -e "${CYAN}A Records:${NC}"
            dig +short A $site | head -3 | sed 's/^/  /'
            
            echo -e "${CYAN}MX Records:${NC}"
            dig +short MX $site | head -3 | sed 's/^/  /'
            ;;
            
        5)
            echo ""
            read -p $'\e[33mEnter website: \e[0m' site
            read -p $'\e[33mEnter port range (e.g., 1-100): \e[0m' range
            
            echo -e "${YELLOW}Scanning ports...${NC}"
            nc -zv $site $range 2>&1 | grep succeeded
            ;;
            
        6)
            echo ""
            read -p $'\e[33mEnter website: \e[0m' site
            
            echo -e "${YELLOW}Fetching HTTP headers...${NC}"
            curl -I "https://$site" 2>/dev/null | head -20
            ;;
            
        0)
            echo ""
            echo -e "${GREEN}Thank you for using Website Checker Tool!${NC}"
            echo -e "${CYAN}Developer: Md. Mainul Islam (MAINUL - X)${NC}"
            echo -e "${CYAN}GitHub: M41NUL | WhatsApp: +8801308850528${NC}"
            break
            ;;
            
        *)
            echo -e "${RED}Invalid option!${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
