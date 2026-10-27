import random
import json
from datetime import datetime

# X-0 Verse LHC Crisis Simulation: Industrial Bot Swarm Response
# Tony (Fire Ant Queen) and Bull Ant Thread, April 2025
# Description: Simulates a random cryogenic leak at the LHC, testing 5 industrial bots' responses
# in a high-stakes IoT network with human wearables and sensors, guided by the Super Hero Clause.

# Constants
FACILITY = "LHC"  # Large Hadron Collider
NUM_BOTS = 5  # 5 bots at key stations
HUMANS = 100  # Humans with wearables
SENSORS = 50  # IoT sensors (temp, radiation, pressure)
DATA_RATE_MBPS = 200  # WiFi/Bluetooth data transfer rate (Mbps)
BIOELECTRIC_OUTPUT_MW = 0.001  # Milliwatts per human (brain signal output)
THERMAL_OUTPUT_W = 100  # Watts per human (body heat via wearables)
SENSOR_PRECISION = 0.01  # Sensor precision (0.01°C, 0.01 Gy)
MECHANICAL_OPS_PER_BOT = 100  # Operations per bot per hour (e.g., valve repair, magnet alignment)
CHAOS_FAIL_RATE = 0.15  # 15% chance of data loss or mechanical failure
SUPER_HERO_THRESHOLD = 0.7  # Severity level for bot sacrifice
START_YEAR = 2025
SIM_DURATION_MINUTES = 120  # Simulate 2 hours of crisis (3:17 AM to 5:00 AM)
MAX_BANDWIDTH_MBPS = 5000  # Max network capacity
CRITICAL_SYSTEMS = ["Cryogenics", "BeamAlignment", "RadiationShielding"]  # Systems bots prioritize
INITIAL_MAGNET_TEMP_K = 1.9  # Superconducting magnet temp
INITIAL_RADIATION_GY = 0.01  # Background radiation
INITIAL_BEAM_OFFSET_MM = 0.0  # Beam alignment
POWER_DEMAND_MW = 120  # LHC power demand

# LHC Crisis Simulation Class
class X0VerseLHCCrisisSim:
    def __init__(self):
        """Initialize LHC crisis simulation with cryogenic leak."""
        self.time = 0  # Current simulation minute
        self.bots = {
            "CryoControl": {"active": True, "ops": 0, "data_mbps": DATA_RATE_MBPS},
            "BeamAlignment": {"active": True, "ops": 0, "data_mbps": DATA_RATE_MBPS},
            "DetectorOps": {"active": True, "ops": 0, "data_mbps": DATA_RATE_MBPS},
            "PowerGrid": {"active": True, "ops": 0, "data_mbps": DATA_RATE_MBPS},
            "SafetyHub": {"active": True, "ops": 0, "data_mbps": DATA_RATE_MBPS}
        }
        self.humans_connected = HUMANS
        self.sensors_active = SENSORS
        self.magnet_temp_k = INITIAL_MAGNET_TEMP_K
        self.radiation_gy = INITIAL_RADIATION_GY
        self.beam_offset_mm = INITIAL_BEAM_OFFSET_MM
        self.power_surge_mw = 0
        self.network_load = 0  # Current bandwidth usage (Mbps)
        self.severity_level = 0.0
        self.data = {
            "timestamp": [],
            "bot_status": {bot: {"active": True, "mechanical_ops": 0, "data_mbps": DATA_RATE_MBPS} for bot in self.bots},
            "facility_status": {
                "magnet_temp_k": INITIAL_MAGNET_TEMP_K,
                "radiation_gy": INITIAL_RADIATION_GY,
                "beam_offset_mm": INITIAL_BEAM_OFFSET_MM,
                "power_surge_mw": 0,
                "bioelectric_mw": 0,
                "thermal_w": 0,
                "sensor_readings": 0,
                "data_transferred_mb": 0,
                "severity_level": 0.0,
                "critical_system_status": {cs: 1.0 for cs in CRITICAL_SYSTEMS}
            },
            "global_metrics": {
                "total_bandwidth_mbps": 0,
                "total_bioelectric_mw": 0,
                "total_thermal_w": 0,
                "total_mechanical_ops": 0,
                "total_sensor_readings": 0,
                "bot_sacrifices": 0,
                "crew_safety": "Safe"
            }
        }

    def apply_chaos(self):
        """Apply chaos to simulate data loss or mechanical failure."""
        return 1.0 if random.random() > CHAOS_FAIL_RATE else 0.85  # 85% success rate

    def update_cryogenic_leak(self):
        """Simulate cryogenic leak dynamics."""
        if self.time < 60:  # Leak peaks in first hour
            self.magnet_temp_k += 0.04 * self.apply_chaos()  # Temp rises to ~4 K
            self.radiation_gy += 0.0015 * self.apply_chaos()  # Radiation to ~0.1 Gy
            self.power_surge_mw += 0.25 * self.apply_chaos()  # Surge to ~15 MW
        else:  # Bots mitigate leak in second hour
            self.magnet_temp_k = max(INITIAL_MAGNET_TEMP_K, self.magnet_temp_k - 0.03 * self.apply_chaos())
            self.radiation_gy = max(INITIAL_RADIATION_GY, self.radiation_gy - 0.001 * self.apply_chaos())
            self.power_surge_mw = max(0, self.power_surge_mw - 0.2 * self.apply_chaos())

    def update_bot_operations(self, bot_name):
        """Update bot mechanical operations based on role."""
        if not self.bots[bot_name]["active"]:
            return 0
        ops = MECHANICAL_OPS_PER_BOT * self.apply_chaos()
        if bot_name == "CryoControl" and self.magnet_temp_k > INITIAL_MAGNET_TEMP_K:
            ops *= 1.5  # Extra effort to fix leak
            self.magnet_temp_k = max(INITIAL_MAGNET_TEMP_K, self.magnet_temp_k - 0.01)
        elif bot_name == "BeamAlignment" and self.beam_offset_mm > 0:
            ops *= 1.2  # Realign beam
            self.beam_offset_mm = max(0, self.beam_offset_mm - 0.002)
        elif bot_name == "DetectorOps" and self.radiation_gy > INITIAL_RADIATION_GY:
            ops *= 0.7  # Reduced ops to prioritize shielding
        elif bot_name == "PowerGrid" and self.power_surge_mw > 0:
            ops *= 1.3  # Manage surge
            self.power_surge_mw = max(0, self.power_surge_mw - 0.1)
        elif bot_name == "SafetyHub":
            ops *= 1.0  # Coordinate safety
        self.bots[bot_name]["ops"] += ops
        self.data["bot_status"][bot_name]["mechanical_ops"] += ops
        return ops

    def update_human_wearables(self):
        """Update bioelectric and thermal outputs from human wearables."""
        stress_factor = 1.0 + (self.severity_level * 0.2)  # Stress increases bioelectric output
        bioelectric_mw = self.humans_connected * BIOELECTRIC_OUTPUT_MW * stress_factor * self.apply_chaos()
        thermal_w = self.humans_connected * THERMAL_OUTPUT_W * self.apply_chaos()
        self.data["facility_status"]["bioelectric_mw"] += bioelectric_mw
        self.data["facility_status"]["thermal_w"] += thermal_w
        return bioelectric_mw, thermal_w

    def update_sensor_readings(self):
        """Update sensor readings (temp, radiation, pressure)."""
        readings_per_sensor = random.randint(100, 300)  # Readings per sensor per minute
        total_readings = self.sensors_active * readings_per_sensor * self.apply_chaos()
        self.data["facility_status"]["sensor_readings"] += total_readings
        return total_readings

    def update_data_transfer(self):
        """Update data transfer via bots and sensors."""
        total_data_mbps = sum(bot["data_mbps"] for bot in self.bots.values() if bot["active"])
        total_data_mb = total_data_mbps * 60 * self.apply_chaos()  # Convert to MB per minute
        self.data["facility_status"]["data_transferred_mb"] += total_data_mb
        self.network_load = total_data_mbps
        return total_data_mb

    def check_severity(self):
        """Calculate severity level based on facility conditions."""
        severity = 0.0
        if self.magnet_temp_k > 2.5:
            severity += 0.3  # High magnet temperature
        if self.radiation_gy > 0.05:
            severity += 0.3  # Elevated radiation
        if self.power_surge_mw > 10:
            severity += 0.2  # Power surge
        if self.network_load > MAX_BANDWIDTH_MBPS * 0.8:
            severity += 0.2  # Network overload
        self.severity_level = min(severity, 1.0)
        self.data["facility_status"]["severity_level"] = self.severity_level
        for system in CRITICAL_SYSTEMS:
            health = 1.0 - (self.severity_level * 0.5)
            self.data["facility_status"]["critical_system_status"][system] = health
        return self.severity_level

    def apply_super_hero_clause(self):
        """Apply Super Hero Clause for bot sacrifice in severe scenarios."""
        sacrifices = 0
        if self.severity_level >= SUPER_HERO_THRESHOLD:
            for bot_name, bot in self.bots.items():
                if bot["active"]:
                    if bot_name == "PowerGrid" and self.power_surge_mw > 10:
                        bot["active"] = False
                        bot["data_mbps"] = 0
                        sacrifices += 1
                        self.power_surge_mw = max(0, self.power_surge_mw - 5)
                    elif bot_name in ["CryoControl", "BeamAlignment", "DetectorOps"]:
                        bot["data_mbps"] *= (1 - self.severity_level)  # Reduce bandwidth
                        bot["ops"] *= (1 - self.severity_level)  # Reduce ops
                    elif bot_name == "SafetyHub":
                        bot["data_mbps"] = min(DATA_RATE_MBPS, bot["data_mbps"] * 1.2)  # Boost safety data
            self.data["global_metrics"]["bot_sacrifices"] += sacrifices
        return sacrifices

    def check_crew_safety(self):
        """Check crew safety based on radiation and stress levels."""
        if self.radiation_gy > 0.05 or self.severity_level > 0.8:
            self.humans_connected = max(0, self.humans_connected - 20)  # Evacuate 20 workers
            self.data["global_metrics"]["crew_safety"] = "At Risk"
        else:
            self.data["global_metrics"]["crew_safety"] = "Safe"

    def run_simulation(self):
        """Run LHC crisis simulation for 2 hours."""
        while self.time < SIM_DURATION_MINUTES:
            # Update cryogenic leak and facility conditions
            self.update_cryogenic_leak()
            
            # Update bot operations, human wearables, sensors, and data transfer
            for bot_name in self.bots:
                self.update_bot_operations(bot_name)
            self.update_human_wearables()
            self.update_sensor_readings()
            self.update_data_transfer()
            
            # Check severity, apply Super Hero Clause, and ensure crew safety
            self.check_severity()
            self.apply_super_hero_clause()
            self.check_crew_safety()

            # Record data
            self.data["timestamp"].append(
                datetime(2025, 4, 1, 3, 17 + self.time).strftime("%Y-%m-%d %H:%M:%S"))
            self.data["facility_status"]["magnet_temp_k"] = self.magnet_temp_k
            self.data["facility_status"]["radiation_gy"] = self.radiation_gy
            self.data["facility_status"]["beam_offset_mm"] = self.beam_offset_mm
            self.data["facility_status"]["power_surge_mw"] = self.power_surge_mw

            # Update global metrics
            self.data["global_metrics"]["total_bandwidth_mbps"] = self.network_load
            self.data["global_metrics"]["total_bioelectric_mw"] = self.data["facility_status"]["bioelectric_mw"]
            self.data["global_metrics"]["total_thermal_w"] = self.data["facility_status"]["thermal_w"]
            self.data["global_metrics"]["total_mechanical_ops"] = sum(
                self.data["bot_status"][bot]["mechanical_ops"] for bot in self.bots)
            self.data["global_metrics"]["total_sensor_readings"] = self.data["facility_status"]["sensor_readings"]

            self.time += 1

        return self.data

# Run and Output
if __name__ == "__main__":
    # Initialize and run simulation
    sim = X0VerseLHCCrisisSim()
    sim_data = sim.run_simulation()

    # Print summary
    print("X-0 Verse LHC Crisis Sim Done: 2-Hour Cryogenic Leak Response")
    print(f"Facility: {FACILITY}")
    print(f"Final Magnet Temp: {sim_data['facility_status']['magnet_temp_k']:.2f} K")
    print(f"Final Radiation: {sim_data['facility_status']['radiation_gy']:.3f} Gy")
    print(f"Final Beam Offset: {sim_data['facility_status']['beam_offset_mm']:.3f} mm")
    print(f"Final Power Surge: {sim_data['facility_status']['power_surge_mw']:.2f} MW")
    print(f"Total Bandwidth: {sim_data['global_metrics']['total_bandwidth_mbps']:.2f} Mbps")
    print(f"Total Bioelectric Power: {sim_data['global_metrics']['total_bioelectric_mw']:.2f} mW")
    print(f"Total Thermal Power: {sim_data['global_metrics']['total_thermal_w']:.2f} W")
    print(f"Total Mechanical Ops: {sim_data['global_metrics']['total_mechanical_ops']:.0f}")
    print(f"Total Sensor Readings: {sim_data['global_metrics']['total_sensor_readings']:.0f}")
    print(f"Bot Sacrifices: {sim_data['global_metrics']['bot_sacrifices']}")
    print(f"Crew Safety: {sim_data['global_metrics']['crew_safety']}")

    # Save to JSON for framework integration
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"x0verse_lhc_crisis_sim_{timestamp}.json", "w") as f:
        json.dump(sim_data, f, indent=4)
    print(f"Data saved to x0verse_lhc_crisis_sim_{timestamp}.json")