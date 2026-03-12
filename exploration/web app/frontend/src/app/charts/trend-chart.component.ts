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
    const fallbackColors = ['#7c6cff', '#38bdf8', '#fb7185', '#34d399', '#f59e0b', '#a78bfa'];
    let fallbackIdx = 0;

    const series: any[] = [];

    this.dealerships.forEach((d, i) => {
      const label = (d.classification?.label ?? '').toUpperCase();
      const baseColor =
        label === 'CHAMPION'
          ? '#22c55e'
          : label === 'STRAGGLER'
            ? '#ef4444'
            : fallbackColors[(fallbackIdx++) % fallbackColors.length];

      // Revenue line
      series.push({
        name: `${d.name} revenue`,
        type: 'line',
        data: d.revenue,
        smooth: true,
        lineStyle: { color: baseColor, width: 2 },
        itemStyle: { color: baseColor },
        symbol: 'circle',
        symbolSize: 4,
      });

      // Trend line (dashed)
      series.push({
        name: `${d.name} trend`,
        type: 'line',
        data: d.trend_line,
        lineStyle: { color: baseColor, type: 'dashed', width: 2.5, opacity: 0.95 },
        itemStyle: { color: baseColor },
        symbol: 'none',
        legendHoverLink: false,
        z: 3,
      });

      // Moving average
      series.push({
        name: `${d.name} MA3`,
        type: 'line',
        data: d.moving_average,
        lineStyle: {
          color: baseColor,
          type: 'dotted',
          width: 3,
          opacity: 0.95,
        },
        itemStyle: { color: baseColor },
        symbol: 'none',
        legendHoverLink: false,
        z: 4,
      });
    });

    this.chartOptions = {
      backgroundColor: 'transparent',
      title: {
        text: `Revenue Trends (${months.length} months)`,
        left: 'center',
        textStyle: { fontSize: 14, color: '#e9eefc' },
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#0f1730',
        borderColor: 'rgba(255,255,255,0.12)',
        textStyle: { color: '#e9eefc' },
      },
      legend: {
        data: this.dealerships.map(d => `${d.name} revenue`),
        bottom: 0,
        textStyle: { color: '#a6b0cf' },
      },
      grid: { left: '5%', right: '3%', bottom: '15%', containLabel: true },
      xAxis: {
        type: 'category',
        data: months,
        boundaryGap: false,
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
        axisLabel: { color: '#a6b0cf' },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      },
      yAxis: {
        type: 'value',
        name: 'Revenue ($k)',
        nameLocation: 'middle',
        nameGap: 50,
        nameTextStyle: { color: '#a6b0cf' },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
        axisLabel: { color: '#a6b0cf' },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      },
      series,
    };
  }
}
