import sys
import json
import asyncio
from typing import Dict, Any

from dffml import op
from dffml import Definition

package = Definition(name="package", primitive="str")
package_version = Definition(name="package_version", primitive="str")
safety_check_number_of_issues = Definition(
    name="safety_check_number_of_issues", primitive="int"
)


@op(
    name="safety_check",
    inputs={"package": package, "version": package_version},
    outputs={"issues": safety_check_number_of_issues},
    conditions=[],
)
async def safety_check(package: str, version: str) -> Dict[str, Any]:
    pinned = f"{package}=={version}"

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "safety",
        "check",
        "--stdin",
        "--json",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, _stderr = await proc.communicate(pinned.encode() + b"\n")

    issues = json.loads(stdout)

    return {"issues": len(issues)}
