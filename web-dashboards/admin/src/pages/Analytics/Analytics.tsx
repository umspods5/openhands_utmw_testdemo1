import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const Analytics: React.FC = () => {
  const usageData = [
    { month: 'Jan', bookings: 120, revenue: 6000 },
    { month: 'Feb', bookings: 150, revenue: 7500 },
    { month: 'Mar', bookings: 180, revenue: 9000 },
    { month: 'Apr', bookings: 200, revenue: 10000 },
    { month: 'May', bookings: 220, revenue: 11000 },
    { month: 'Jun', bookings: 250, revenue: 12500 },
  ];

  const lockerUsageData = [
    { size: 'Small', usage: 45 },
    { size: 'Medium', usage: 35 },
    { size: 'Large', usage: 20 },
  ];

  const itemTypeData = [
    { name: 'Parcels', value: 40, color: '#8884d8' },
    { name: 'Food', value: 30, color: '#82ca9d' },
    { name: 'Documents', value: 20, color: '#ffc658' },
    { name: 'Laundry', value: 10, color: '#ff7300' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Monthly Bookings & Revenue
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={usageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Bar yAxisId="left" dataKey="bookings" fill="#8884d8" />
                <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Item Types Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={itemTypeData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {itemTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Locker Size Usage
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={lockerUsageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="size" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="usage" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;