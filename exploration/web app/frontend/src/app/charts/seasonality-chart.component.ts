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
      title: {
        text: `Seasonality Decomposition — ${this.data.dealership}`,
        subtext: `Seasonal strength: ${this.data.summary.seasonal_strength_pct}%  |  Peak: M${this.data.summary.peak_month}  |  Trough: M${this.data.summary.trough_month}`,
        left: 'center',
        textStyle: { fontSize: 14 },
        subtextStyle: { fontSize: 11 },
      },
      tooltip: { trigger: 'axis' },
      legend: {
        data: ['Observed', 'Trend', 'Seasonal', 'Residual'],
        bottom: 0,
      },
      grid: { left: '5%', right: '3%', bottom: '15%', containLabel: true },
      xAxis: { type: 'category', data: months, boundaryGap: false },
      yAxis: { type: 'value', name: 'Value ($k)', nameLocation: 'middle', nameGap: 50 },
      series: [
        {
          name: 'Observed',
          type: 'line',
          data: this.data.observed,
          smooth: true,
          lineStyle: { width: 2, color: '#4e79a7' },
          itemStyle: { color: '#4e79a7' },
          symbolSize: 4,
        },
        {
          name: 'Trend',
          type: 'line',
          data: this.data.trend,
          smooth: true,
          lineStyle: { width: 2, color: '#f28e2b' },
          itemStyle: { color: '#f28e2b' },
          symbol: 'none',
        },
        {
          name: 'Seasonal',
          type: 'line',
          data: this.data.seasonal,
          smooth: true,
          lineStyle: { width: 1.5, color: '#59a14f', type: 'dashed' },
          itemStyle: { color: '#59a14f' },
          symbol: 'none',
        },
        {
          name: 'Residual',
          type: 'line',
          data: this.data.residual,
          smooth: false,
          lineStyle: { width: 1, color: '#b07aa1', type: 'dotted' },
          itemStyle: { color: '#b07aa1' },
          symbol: 'none',
        },
      ],
    };
  }
}
