"""Visualization status and all used urls"""
import json
import datetime
import io
import xlsxwriter

from Products.Five.browser import BrowserView
from plone import api


class VisualizationUsage(BrowserView):
    """Visualizations usage and status"""

    def __call__(self):
        visualizations = self.get_visualizations()

        start = self.safe_int(self.request.get('b_start'), 0)
        size = self.safe_int(self.request.get('b_size'), 10)

        total = len(visualizations)
        end = start + size
        items = list(visualizations.items())
        sliced = items[start:end]

        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps({
            "data": dict(sliced), "count": total,
        })

    def get_visualizations(self):
        """Get visualizations and gather all usages"""
        result = api.content.find(portal_type="visualization")
        data = {}

        for brain in result:
            obj = brain.getObject()
            path = {
                "id": obj.id,
                "uid": obj.UID(),
                "url": brain.getURL(),
                "path": brain.getPath().replace("/Plone", ""),
                "review_state": brain.review_state,
                "created": obj.ModificationDate(),
                "modified": obj.CreationDate(),
                "title": obj.Title(),
                "type_title": obj.portal_type
            }
            if obj.id in data:
                data[obj.id].append(path)
            else:
                data[obj.id] = [path]

        return data

    def safe_int(self, value, default):
        """Safe format to int"""
        try:
            return max(0, int(value))
        except (ValueError, TypeError):
            return default

    def export_to_xlsx(self):
        """Export visualizations relationships to xlsx"""
        visualizations = self.get_visualizations()

        out = io.BytesIO()
        workbook = xlsxwriter.Workbook(out, {'in_memory': True})

        # add worksheet with report header data
        worksheet = workbook.add_worksheet('Relationships')

        headers = ['Visualization Title', 'Visualization URL', 'Review state']

        for i, title in enumerate(headers):
            worksheet.write(0, i, title)

        i = 0
        for _, items in visualizations.items():
            for viz in items:
                worksheet.write(i + 1, 0, viz['title'])
                worksheet.write(i + 1, 1, viz['url'])
                worksheet.write(i + 1, 2, viz['review_state'])
                i += 1

        workbook.close()
        out.seek(0)

        sh = self.request.response.setHeader

        sh('Content-Type', 'application/vnd.openxmlformats-officedocument.'
           'spreadsheetml.sheet')
        fname = "-".join(('Visualization Usage',
                          datetime.datetime.now().strftime('%Y-%m-%d')))
        sh('Content-Disposition', 'attachment; filename=%s.xlsx' % fname)

        return out.read()
