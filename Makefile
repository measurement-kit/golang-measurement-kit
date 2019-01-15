testdata/GeoLite2-ASN.mmdb:
	cd testdata && curl -fsSLO https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz
	cd testdata && tar xzf GeoLite2-ASN.tar.gz && rm GeoLite2-ASN.tar.gz
	mv testdata/GeoLite2-ASN_*/GeoLite2-ASN.mmdb testdata/ && rm -rf testdata/GeoLite2-ASN_*/

testdata/GeoLite2-Country.mmdb:
	cd testdata && curl -fsSLO https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz
	cd testdata && tar xzf GeoLite2-Country.tar.gz && rm GeoLite2-Country.tar.gz
	mv testdata/GeoLite2-Country_*/GeoLite2-Country.mmdb testdata/ && rm -rf testdata/GeoLite2-Country_*/

testdata: testdata/GeoLite2-Country.mmdb testdata/GeoLite2-ASN.mmdb

.PHONY: testdata

test: testdata
	go test -v ./...
