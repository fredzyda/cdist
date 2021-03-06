#!/bin/sh

cat <<EOF
# Auto-generated by cdist __samplereturn_network
# Please edit template
auto lo
iface lo inet loopback

auto ${WIRED_INTERFACE}
iface ${WIRED_INTERFACE} inet static
 address ${WIRED_IP}
 netmask ${WIRED_NM}
EOF
if [ -n "${WIRED_GW}" ]; then
    echo " gateway ${WIRED_GW}"
fi

if [ -n "${WIRED_NS}" ]; then
    echo " dns-nameservers ${WIRED_NS}"
fi
if [ -n "${WIRED_ROUTES}" ]; then
    echo ${WIRED_ROUTES}
fi

if [ -n "${WIRELESS_IP}" ]; then
cat <<EOF
allow-hotplug wlan0
iface wlan0 inet static
  wireless-mode ad-hoc
  wireless-channel ${WIRELESS_CHANNEL}
  wireless-essid ${WIRELESS_SSID}
  wireless-key ${WIRELESS_KEY}
  address ${WIRELESS_IP}
  netmask ${WIRELESS_NM}
EOF
fi

