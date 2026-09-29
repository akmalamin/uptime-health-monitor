"""engine/incident_logger.py — Records logs and exports color-coded Excel reports."""

import os
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from config import Config


class IncidentLogger:
    """Records monitoring metrics and exports branded Excel health audits."""

    def __init__(self):
        self.logs = []

    def record(self, result):
        self.logs.append(result)

    def export_excel_report(self):
        if not self.logs:
            print("   ⚠️ No audit logs to export")
            return None

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Uptime_Health_Report_{ts}.xlsx"
        output_path = os.path.join(Config.OUTPUT_DIR, filename)

        df = pd.DataFrame(self.logs)

        wb = Workbook()
        ws = wb.active
        ws.title = "System Health Audit"

        # Styles
        header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
        thin_border = Border(
            left=Side(style="thin", color="CBD5E0"),
            right=Side(style="thin", color="CBD5E0"),
            top=Side(style="thin", color="CBD5E0"),
            bottom=Side(style="thin", color="CBD5E0"),
        )

        # Title Block
        ws.merge_cells("A1:H1")
        ws["A1"].value = "ENTERPRISE UPTIME & SYSTEM HEALTH REPORT"
        ws["A1"].font = Font(name="Calibri", bold=True, size=14, color="1A365D")
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:H2")
        ws["A2"].value = f"Audit Run: {datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')} | Total Probes: {len(df)}"
        ws["A2"].font = Font(name="Calibri", italic=True, size=10, color="718096")
        ws["A2"].alignment = Alignment(horizontal="center")

        # Table Headers
        headers = ["Target Name", "Endpoint URL", "Category", "Timestamp", "HTTP Code", "Latency (ms)", "Status", "Details / Error"]
        start_row = 4

        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col_num, value=header_title)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        # Populate Data Rows
        for r_idx, item in enumerate(self.logs, start=start_row + 1):
            row_data = [
                item["name"],
                item["url"],
                item["category"],
                item["timestamp"],
                item["status_code"] if item["status_code"] != 0 else "N/A",
                item["latency_ms"],
                item["health_label"],
                item["error_reason"] or "All systems operational",
            ]

            for c_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=val)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                # Color-code Health Status Column
                if c_idx == 7:
                    cell.alignment = Alignment(horizontal="center")
                    if "HEALTHY" in str(val):
                        cell.fill = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")  # Green
                        cell.font = Font(name="Calibri", bold=True, color="22543D")
                    elif "DEGRADED" in str(val):
                        cell.fill = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")  # Yellow
                        cell.font = Font(name="Calibri", bold=True, color="744210")
                    else:
                        cell.fill = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")  # Red
                        cell.font = Font(name="Calibri", bold=True, color="742A2A")

        # Auto-adjust column widths
        for col in ws.columns:
            max_len = max(len(str(c.value or "")) for c in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max_len + 3, 45)

        wb.save(output_path)
        print(f"\n💾 Health Report generated → {output_path}")
        return output_path