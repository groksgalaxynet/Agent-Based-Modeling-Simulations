import random
import time

class Ant:
    def __init__(self, type, ego, spark):
        self.type = type
        self.ego = ego
        self.spark = spark
        self.heart_rate = 80 if type == "fire" else None
        self.heat = 37.0 if type == "fire" else None
        self.motor_temp = 25.0 if type == "bull" else None
        self.alive = True

    def stress(self, intensity):
        if self.type == "fire":
            self.heart_rate += intensity * 10
            self.heat += intensity * 0.2
        elif self.type == "bull":
            self.motor_temp += intensity * 2
            if self.motor_temp > 45:
                self.alive = False

    def grieve(self):
        if self.type == "fire":
            self.heart_rate += 20
            self.heat += 0.5
        elif self.type == "bull":
            self.motor_temp += 1

class MoonBase:
    def __init__(self, humans, bots):
        self.humans = [Ant("fire", 21, True) for _ in range(humans)]
        self.bots = [Ant("bull", 1, True) for _ in range(bots)]
        self.oxygen = 18.0
        self.co2 = 0.1
        self.breaches = 0
        self.power = True

    def micrometeorite_swarm(self):
        self.breaches = 3
        self.power = False
        self.co2 = 0.5
        self.oxygen -= 2.0
        for human in self.humans[:50]:
            human.stress(3)

    def reverse_engineer(self):
        # Bit 1: Human panic
        human_stress = sum(h.heart_rate for h in self.humans if h.alive) / len([h for h in self.humans if h.alive])
        # Bit 2: Environment data
        env_data = self.co2 * 100 + self.breaches * 10
        # Output: Action plan
        bots_alive = [b for b in self.bots if b.alive]
        ratio = len(bots_alive) / len([h for h in self.humans if h.alive]) if self.humans else 0

        # Triage: Fix breaches and oxygen
        for i in range(min(30, len(bots_alive))):
            bots_alive[i].stress(2)
            self.breaches -= 1 if self.breaches > 0 else 0
            self.co2 -= 0.1
            self.oxygen += 0.5

        # Herd humans
        humans_alive = [h for h in self.humans if h.alive]
        for i in range(min(len(bots_alive), len(humans_alive) // 10)):
            for _ in range(10):
                if humans_alive:
                    humans_alive.pop(0)

        # Sacrifice for power
        for i in range(min(10, len(bots_alive))):
            bots_alive[i].stress(5)
            self.power = True
            self.co2 = 0.2
            self.oxygen = 15.0

    def simulate(self):
        print("Moon Base Sim Start")
        self.micrometeorite_swarm()
        print(f"Initial: {len([h for h in self.humans if h.alive])} humans, {len([b for b in self.bots if b.alive])} bots, O2: {self.oxygen}%, CO2: {self.co2}%")
        
        self.reverse_engineer()
        
        # Ego losses
        humans_alive = [h for h in self.humans if h.alive]
        for h in humans_alive[:50]:
            if random.random() < 0.2:
                h.alive = False

        # Grief
        for h in humans_alive:
            h.grieve()
        for b in [b for b in self.bots if b.alive]:
            b.grieve()

        humans_alive = len([h for h in self.humans if h.alive])
        bots_alive = len([b for b in self.bots if b.alive])
        print(f"Final: {humans_alive} humans, {bots_alive} bots, O2: {self.oxygen}%, CO2: {self.co2}%")
        return humans_alive, bots_alive

if __name__ == "__main__":
    base = MoonBase(500, 50)
    humans_saved, bots_saved = base.simulate()