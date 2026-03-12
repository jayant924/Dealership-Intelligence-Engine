import { Component, Input, OnChanges } from '@angular/core';
import { NgxEchartsDirective, provideEchartsCore } from 'ngx-echarts';
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  GridComponent, TooltipComponent, LegendComponent, TitleComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { DealershipSeasonality } from '../services/intelligence.service';

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent, CanvasRenderer]);

@Component({
  selector: 'app-seasonality-chart',
  standalone: true,
  imports: [NgxEchartsDirective],
  providers: [provideEchartsCore({ echarts })],
  template: `
    <div echarts [options]="chartOptions" style="height: 320px; width: 100%;"></div>
  `,
})
export class SeasonalityChartComponent implements OnChanges {
  @Input() data!: DealershipSeasonality;

  chartOptions: any = {};

  ngOnChanges() {
    if (!this.data) return;
    this.buildChart();
  }

  private buildChart() {
    const months = this.data.months.map(m => `M${m}`);

    this.chartOptions = {
      backgroundColor: 'transparent',
      title: {
        text: `Seasonality Decomposition — ${this.data.dealership}`,
        subtext: `Seasonal strength: ${this.data.summary.seasonal_strength_pct}%  |  Peak: M${this.data.summary.peak_month}  |  Trough: M${this.data.summary.trough_month}`,
        left: 'center',
        textStyle: { fontSize: 14, color: '#e9eefc' },
        subtextStyle: { fontSize: 11, color: '#a6b0cf' },
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#0f1730',
        borderColor: 'rgba(255,255,255,0.12)',
        textStyle: { color: '#e9eefc' },
      },
      legend: {
        data: ['Observed', 'Trend', 'Seasonal', 'Residual'],
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
        name: 'Value ($k)',
        nameLocation: 'middle',
        nameGap: 50,
        nameTextStyle: { color: '#a6b0cf' },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.16)' } },
        axisLabel: { color: '#a6b0cf' },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      },
      series: [
        {
          name: 'Observed',
          type: 'line',
          data: this.data.observed,
          smooth: true,
          lineStyle: { width: 2, color: '#38bdf8' },
          itemStyle: { color: '#38bdf8' },
          symbolSize: 4,
        },
        {
          name: 'Trend',
          type: 'line',
          data: this.data.trend,
          smooth: true,
          lineStyle: { width: 2, color: '#7c6cff' },
          itemStyle: { color: '#7c6cff' },
          symbol: 'none',
        },
        {
          name: 'Seasonal',
          type: 'line',
          data: this.data.seasonal,
          smooth: true,
          lineStyle: { width: 1.5, color: '#34d399', type: 'dashed' },
          itemStyle: { color: '#34d399' },
          symbol: 'none',
        },
        {
          name: 'Residual',
          type: 'line',
          data: this.data.residual,
          smooth: false,
          lineStyle: { width: 1, color: '#fb7185', type: 'dotted' },
          itemStyle: { color: '#fb7185' },
          symbol: 'none',
        },
      ],
    };
  }
}
