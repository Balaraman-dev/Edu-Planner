import yaml

class SkillTree:
    def __init__(self, process_mgmt=3, memory_mgmt=2, fs=4, scheduling=3, sync=2):
        self.levels = {
            "process_management": process_mgmt,
            "memory_management": memory_mgmt,
            "file_systems": fs,
            "cpu_scheduling": scheduling,
            "synchronization_deadlocks": sync
        }

    def set_level(self, dim: str, level: int):
        if dim in self.levels and 1 <= level <= 5:
            self.levels[dim] = level

    def get_summary(self) -> str:
        return "; ".join([f"{k}: Level {v}" for k, v in self.levels.items()])

    def load_from_yaml(self, yaml_path: str):
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            for key, value in data.items():
                if key in self.levels:
                    self.levels[key] = value
