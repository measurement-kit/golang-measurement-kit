package mk

import (
	"testing"
	"fmt"
)

func TestFacebookMessenger(t *testing.T) {
	nt = NewNettest("FacebookMessenger")
	nt.Options = NettestOptions{
		DisableCollector: true,
		GeoIPASNPath: "GeoLite2-ASN.mmdb",
		GeoIPCountryPath: "GeoLite2-Country.mmdb",
		OutputPath: "facebook-result.jsonl",
	}
	nt.On("*", func(e mk.Event) {
		fmt.Printf("%v\n", e)
	})
	nt.Run()
}
