import { Component, Input, OnChanges } from '@angular/core';
import { NgxEchartsDirective, provideEchartsCore } from 'ngx-echarts';
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  GridComponent, TooltipComponent, LegendComponent, TitleComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { DealershipTrend } from '../services/intelligence.service';

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent, CanvasRenderer]);

@Component({
  selector: 'app-trend-chart',
  standalone: true,
  imports: [NgxEchartsDirective],
  providers: [provideEchartsCore({ echarts })],
  template: `
    <div echarts [options]="chartOptions" style="height: 320px; width: 100%;"></div>
  `,
})
export class TrendChartComponent implements OnChanges {
  @Input() dealerships: DealershipTrend[] = [];

  chartOptions: any = {};

  ngOnChanges() {
    if (!this.dealerships.length) return;
    this.buildChart();
  }

  private buildChart() {
    const months = this.dealerships[0].months.map(m => `M${m}`);
    const colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2'];

    const series: any[] = [];

    this.dealerships.forEach((d, i) => {
      // Revenue line
      series.push({
        name: `${d.name} revenue`,
        type: 'line',
        data: d.revenue,
        smooth: true,
        lineStyle: { color: colors[i], width: 2 },
        itemStyle: { color: colors[i] },
        symbol: 'circle',
        symbolSize: 4,
      });

      // Trend line (dashed)
      series.push({
        name: `${d.name} trend`,
        type: 'line',
        data: d.trend_line,
        lineStyle: { color: colors[i], type: 'dashed', width: 1, opacity: 0.6 },
        itemStyle: { color: colors[i] },
        symbol: 'none',
        legendHoverLink: false,
      });

      // Moving average
      series.push({
        name: `${d.name} MA3`,
        type: 'line',
        data: d.moving_average,
        lineStyle: { color: colors[i], type: 'dotted', width: 1.5 },
        itemStyle: { color: colors[i] },
        symbol: 'none',
        legendHoverLink: false,
      });
    });

    this.chartOptions = {
      title: { text: 'Revenue Trends (24 months)', left: 'center', textStyle: { fontSize: 14 } },
      tooltip: { trigger: 'axis' },
      legend: {
        data: this.dealerships.map(d => `${d.name} revenue`),
        bottom: 0,
      },
      grid: { left: '5%', right: '3%', bottom: '15%', containLabel: true },
      xAxis: { type: 'category', data: months, boundaryGap: false },
      yAxis: { type: 'value', name: 'Revenue ($k)', nameLocation: 'middle', nameGap: 50 },
      series,
    };
  }
}
