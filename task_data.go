package mk

import "C"
import (
	"encoding/json"
	"unsafe"
)

func mkBoolOption(v bool) int {
	if v == true {
		return 1
	}
	return 0
}

// TaskData contains the measurement_kit task_data structure
type TaskData struct {
	DisabledEvents []string              `json:"disabled_events,omitempty"`
	Name           string                `json:"name"`
	LogLevel       string                `json:"verbosity,omitempty"`
	Options        measurementKitOptions `json:"options"`
}

type measurementKitOptions struct {
	SaveRealProbeIP  int    `json:"save_real_probe_ip,omitempty"`
	SaveRealProbeASN int    `json:"save_real_probe_asn,omitempty"`
	SaveRealProbeCC  int    `json:"save_real_probe_cc,omitempty"`
	NoCollector      int    `json:"no_collector,omitempty"`
	SoftwareName     string `json:"software_name,omitempty"`
	SoftwareVersion  string `json:"software_version,omitempty"`

	GeoIPCountryPath string `json:"geoip_country_path,omitempty"`
	GeoIPASNPath     string `json:"geoip_asn_path,omitempty"`
	OutputFilePath   string `json:"output_filepath,omitempty"`
	CaBundlePath     string `json:"net/ca_bundle_path,omitempty"`
}

// MakeTaskData returns a pointer to a TaskData structure
func MakeTaskData(nt *Nettest) (*TaskData, error) {
	logLevel := nt.Options.LogLevel
	if nt.Options.LogLevel == "" {
		logLevel = "INFO"
	}

	td := TaskData{
		Name:     nt.Name,
		LogLevel: logLevel,
		Options: measurementKitOptions{
			SaveRealProbeIP:  mkBoolOption(nt.Options.IncludeIP),
			SaveRealProbeASN: mkBoolOption(nt.Options.IncludeASN),
			SaveRealProbeCC:  mkBoolOption(nt.Options.IncludeCountry),
			NoCollector:      mkBoolOption(nt.Options.DisableCollector),

			SoftwareName:    nt.Options.SoftwareName,
			SoftwareVersion: nt.Options.SoftwareVersion,

			GeoIPCountryPath: nt.Options.GeoIPCountryPath,
			GeoIPASNPath:     nt.Options.GeoIPASNPath,
			OutputFilePath:   nt.Options.OutputPath,
			CaBundlePath:     nt.Options.CaBundlePath,
		},
	}
	if nt.DisabledEvents != nil {
		td.DisabledEvents = nt.DisabledEvents
	} else {
		td.DisabledEvents = make([]string, 0)
	}
	return &td, nil
}

// ToPointer converts a TaskData object to a C style pointer
func (td *TaskData) ToPointer() (*C.char, error) {
	tdBytes, err := json.Marshal(td)
	if err != nil {
		return nil, err
	}
	return (*C.char)(unsafe.Pointer(&tdBytes[0])), nil
}
