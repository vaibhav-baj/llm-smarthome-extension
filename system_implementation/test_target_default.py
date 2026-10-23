"""An omitted target argument takes its declared default (no LLM, simulator or Lean needed).

Run from system_implementation/:
    python -m unittest test_target_default
"""
import unittest

import smart_home_langgraph as shl


def state(service_schema):
    operation = {"parameters": {"service_id": service_schema, "name": {"type": "string"}},
                 "reads": ["device.x.state"], "writes": ["device.x.state"], "preconditions": []}
    return {"agent_registry": {"lighting": {"operations": {"HassTurnOn": operation}}}, "action_graph": {}}


def action(**arguments):
    return {"task": {"agent_id": "lighting"}, "skill_id": "HassTurnOn", "arguments": arguments}


class TargetDefaultTests(unittest.TestCase):

    def test_omitted_service_takes_declared_default(self):
        s, a = state({"type": "string", "enum": ["light"], "default": "light"}), action(name="Kitchen Light")
        shl.fill_target_default(s, a)
        self.assertEqual(a["arguments"], {"service_id": "light", "name": "Kitchen Light"})
        self.assertEqual(shl.action_footprint(s, a)[2], ("service_id", "light"))

    def test_given_service_is_kept(self):
        s, a = state({"type": "string", "default": "light"}), action(service_id="other", name="x")
        shl.fill_target_default(s, a)
        self.assertEqual(a["arguments"]["service_id"], "other")

    def test_without_default_behaviour_is_unchanged(self):
        s, a = state({"type": "string"}), action(name="x")
        shl.fill_target_default(s, a)
        self.assertNotIn("service_id", a["arguments"])
        with self.assertRaises(KeyError):
            shl.action_footprint(s, a)


if __name__ == "__main__":
    unittest.main()
